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
    LLM_COMPLETED
)

from document_repository import DocumentRepository
from services.text_splitter import TextSplitter
from services.chroma_service import ChromaService


KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC = LLM_COMPLETED


# ============================================================
# PROMETHEUS METRICS
# ============================================================

documents_received = Counter(
    "documents_received_total",
    "Total number of documents received by embedding worker"
)

documents_processed = Counter(
    "documents_processed_total",
    "Total number of documents processed by embedding worker"
)

documents_success = Counter(
    "documents_success_total",
    "Total number of successfully embedded documents"
)

documents_failed = Counter(
    "documents_failed_total",
    "Total number of failed embedding documents"
)

documents_processing = Gauge(
    "documents_processing",
    "Number of documents currently being embedded"
)

embedding_duration = Histogram(
    "embedding_duration_seconds",
    "Embedding and ChromaDB storage duration in seconds"
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

                group_id="snrt-embedding-worker-v1",

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
                "🧠 Embedding Worker started...",
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

    splitter = TextSplitter()

    chroma = ChromaService()

    consumer = await create_consumer()

    await kafka_producer.start()

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
                    "Document ID :",
                    document_id,
                    flush=True
                )

                # ====================================================
                # LOAD TEXT FROM MONGODB
                # ====================================================

                print(
                    "📄 Loading text...",
                    flush=True
                )

                text = await repository.get_text(

                    document_id

                )

                if not text:

                    print(
                        "❌ Text not found",
                        flush=True
                    )

                    documents_failed.inc()

                    continue

                print(
                    "✅ Text loaded successfully",
                    flush=True
                )

                # ====================================================
                # TEXT SPLITTING
                # ====================================================

                print(
                    "✂ Splitting text...",
                    flush=True
                )

                chunks = splitter.split(

                    text

                )

                print(
                    f"✅ {len(chunks)} chunks created",
                    flush=True
                )

                # ====================================================
                # CHROMADB / EMBEDDINGS
                # ====================================================

                print(
                    "📦 Storing chunks into ChromaDB...",
                    flush=True
                )

                embedding_start = time.perf_counter()

                await asyncio.to_thread(

                    chroma.add_document,

                    document_id,

                    chunks

                )

                embedding_time = (

                    time.perf_counter()
                    - embedding_start

                )

                embedding_duration.observe(

                    embedding_time

                )

                print(
                    f"⏱️ Embedding duration: "
                    f"{embedding_time:.2f}s",
                    flush=True
                )

                print(
                    "✅ Chunks stored",
                    flush=True
                )

                # ====================================================
                # CHROMA COUNT
                # ====================================================

                count = chroma.count_documents()

                print(
                    f"📊 Total chunks in Chroma : {count}",
                    flush=True
                )

                # ====================================================
                # MONGODB STATUS
                # ====================================================

                await repository.update_embedding_status(

                    document_id

                )

                print(
                    "✅ MongoDB updated",
                    flush=True
                )

                # ====================================================
                # TOTAL PROCESSING TIME
                # ====================================================

                total_time = (

                    time.perf_counter()
                    - start_time

                )

                print(
                    f"⏱️ Total embedding processing: "
                    f"{total_time:.2f}s",
                    flush=True
                )

                documents_success.inc()

                print(
                    "✅ Embedding document processed successfully",
                    flush=True
                )

            except Exception as e:

                documents_failed.inc()

                worker_errors.inc()

                print(
                    f"❌ Error processing embedding: {e}",
                    flush=True
                )

            finally:

                documents_processed.inc()

                documents_processing.dec()

    finally:

        await kafka_producer.stop()

        await consumer.stop()

        print(
            "🛑 Embedding Worker stopped",
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