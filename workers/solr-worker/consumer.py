import asyncio
import json
import time

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    start_http_server
)

from topics import LLM_COMPLETED

from document_repository import DocumentRepository
from solr_service import SolrService


KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC = LLM_COMPLETED


# ============================================================
# PROMETHEUS METRICS
# ============================================================

documents_received = Counter(
    "documents_received_total",
    "Total number of documents received by Solr worker"
)

documents_processed = Counter(
    "documents_processed_total",
    "Total number of documents processed by Solr worker"
)

documents_success = Counter(
    "documents_success_total",
    "Total number of successfully indexed documents"
)

documents_failed = Counter(
    "documents_failed_total",
    "Total number of failed Solr indexation documents"
)

documents_processing = Gauge(
    "documents_processing",
    "Number of documents currently being indexed in Solr"
)

solr_indexation_duration = Histogram(
    "solr_indexation_duration_seconds",
    "Solr document indexation duration in seconds"
)

worker_errors = Counter(
    "worker_errors_total",
    "Total number of Solr worker errors"
)


# ============================================================
# KAFKA CONSUMER
# ============================================================

async def create_consumer():

    while True:

        consumer = None

        try:

            print(
                "⏳ Connecting to Kafka...",
                flush=True
            )

            consumer = AIOKafkaConsumer(
                TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                group_id="snrt-solr-worker-v1",
                auto_offset_reset="earliest"
            )

            await consumer.start()

            topics = await consumer.topics()

            print(
                f"✅ Kafka connected. Available topics: {topics}",
                flush=True
            )

            if TOPIC not in topics:

                print(
                    f"❌ Topic {TOPIC} does not exist",
                    flush=True
                )

                await consumer.stop()

                await asyncio.sleep(5)

                continue

            print(
                "🔎 Solr Worker started...",
                flush=True
            )

            print(
                "Waiting for LLM results...",
                flush=True
            )

            return consumer

        except KafkaConnectionError as e:

            print(
                f"⏳ Kafka not ready: {e}",
                flush=True
            )

            worker_errors.inc()

            if consumer:
                await consumer.stop()

            await asyncio.sleep(5)


# ============================================================
# CONSUMER
# ============================================================

async def consume():

    repository = DocumentRepository()

    solr = SolrService()

    consumer = await create_consumer()

    try:

        async for message in consumer:

            documents_received.inc()

            documents_processing.inc()

            start_time = time.perf_counter()

            try:

                print(
                    "\n📩 New LLM result received",
                    flush=True
                )

                data = json.loads(
                    message.value.decode("utf-8")
                )

                document_id = data.get(
                    "document_id"
                )

                print(
                    f"Document ID : {document_id}",
                    flush=True
                )

                print(
                    "📄 Loading document from MongoDB...",
                    flush=True
                )

                document = await repository.get_document(
                    document_id
                )

                if document is None:

                    print(
                        "❌ Document not found",
                        flush=True
                    )

                    documents_failed.inc()

                    continue

                solr_document = {

                    "id": str(
                        document["_id"]
                    ),

                    "title": document.get(
                        "title"
                    ),

                    "transcription": document.get(
                        "transcription"
                    ),

                    "summary": document.get(
                        "ai_metadata",
                        {}
                    ).get(
                        "summary"
                    ),

                    "keywords": document.get(
                        "ai_metadata",
                        {}
                    ).get(
                        "keywords",
                        []
                    )

                }

                print(
                    "📦 Sending document to Solr...",
                    flush=True
                )

                # ------------------------------------------------
                # SOLR INDEXATION TIMER
                # ------------------------------------------------

                solr_start = time.perf_counter()

                await asyncio.to_thread(
                    solr.index_document,
                    solr_document
                )

                solr_time = (
                    time.perf_counter()
                    - solr_start
                )

                solr_indexation_duration.observe(
                    solr_time
                )

                print(
                    f"⏱️ Solr indexation duration: "
                    f"{solr_time:.2f}s",
                    flush=True
                )

                print(
                    "✅ Indexed in Solr",
                    flush=True
                )

                # ------------------------------------------------
                # UPDATE MONGODB
                # ------------------------------------------------

                await repository.update_solr_status(
                    document_id
                )

                print(
                    "✅ MongoDB updated",
                    flush=True
                )

                total_time = (
                    time.perf_counter()
                    - start_time
                )

                print(
                    f"⏱️ Total Solr processing: "
                    f"{total_time:.2f}s",
                    flush=True
                )

                documents_success.inc()

                print(
                    "✅ Solr document processed successfully",
                    flush=True
                )

            except Exception as e:

                documents_failed.inc()

                worker_errors.inc()

                print(
                    f"❌ Error processing Solr document: {e}",
                    flush=True
                )

            finally:

                documents_processed.inc()

                documents_processing.dec()

    finally:

        await consumer.stop()

        print(
            "🛑 Solr Worker stopped",
            flush=True
        )


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    start_http_server(8000)

    print(
        "📊 Prometheus metrics available on port 8000",
        flush=True
    )

    asyncio.run(
        consume()
    )