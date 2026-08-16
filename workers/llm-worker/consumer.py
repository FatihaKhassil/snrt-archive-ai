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

from kafka_producer import kafka_producer
from topics import (
    TEXT_EXTRACTED,
    LLM_COMPLETED
)

from llm_service import LLMService
from document_repository import DocumentRepository


KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC = TEXT_EXTRACTED


# ============================================================
# PROMETHEUS METRICS
# ============================================================

documents_received = Counter(
    "documents_received_total",
    "Total number of documents received by LLM worker"
)

documents_processed = Counter(
    "documents_processed_total",
    "Total number of documents processed by LLM worker"
)

documents_success = Counter(
    "documents_success_total",
    "Total number of successfully processed documents"
)

documents_failed = Counter(
    "documents_failed_total",
    "Total number of failed documents"
)

documents_processing = Gauge(
    "documents_processing",
    "Number of documents currently being processed"
)

llm_duration = Histogram(
    "llm_duration_seconds",
    "LLM processing duration in seconds"
)

worker_errors = Counter(
    "worker_errors_total",
    "Total number of worker errors"
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
                group_id="snrt-llm-worker-v1",
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
                "🤖 LLM Worker started...",
                flush=True
            )

            print(
                "Waiting for extracted texts...",
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
# CONSUMER LOOP
# ============================================================

async def consume():

    llm_service = LLMService()

    repository = DocumentRepository()

    consumer = await create_consumer()

    await kafka_producer.start()

    try:

        async for message in consumer:

            documents_received.inc()

            documents_processing.inc()

            start_time = time.perf_counter()

            try:

                print(
                    "\n📩 New extracted text received",
                    flush=True
                )

                data = json.loads(
                    message.value.decode("utf-8")
                )

                document_id = data.get(
                    "document_id"
                )

                text = data.get(
                    "text"
                )

                print(
                    "Document ID :",
                    document_id,
                    flush=True
                )

                print(
                    "🤖 Starting LLM processing...",
                    flush=True
                )

                print(
                    "📝 Building prompt...",
                    flush=True
                )

                result = await asyncio.to_thread(

                    llm_service.process,

                    text

                )

                duration = (
                    time.perf_counter()
                    - start_time
                )

                llm_duration.observe(
                    duration
                )

                print(
                    f"⏱️ LLM duration: {duration:.2f}s",
                    flush=True
                )

                print(
                    "✅ LLM processing completed",
                    flush=True
                )

                await repository.update_llm_result(

                    document_id,

                    result["summary"],

                    result["keywords"]

                )

                print(
                    "✅ Metadata saved to MongoDB",
                    flush=True
                )

                print(
                    "Summary :",
                    result["summary"],
                    flush=True
                )

                print(
                    "Keywords :",
                    result["keywords"],
                    flush=True
                )

                print(
                    "📤 Sending metadata to Kafka...",
                    flush=True
                )

                await kafka_producer.send(

                    LLM_COMPLETED,

                    {
                        "document_id": document_id,
                        "summary": result["summary"],
                        "keywords": result["keywords"]
                    }

                )

                print(
                    "✅ Metadata sent",
                    flush=True
                )

                documents_success.inc()

                print(
                    "✅ LLM document processed successfully",
                    flush=True
                )

            except Exception as e:

                documents_failed.inc()

                worker_errors.inc()

                print(
                    f"❌ Error processing document: {e}",
                    flush=True
                )

            finally:

                documents_processed.inc()

                documents_processing.dec()

    finally:

        await kafka_producer.stop()

        await consumer.stop()

        print(
            "🛑 LLM Worker stopped",
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