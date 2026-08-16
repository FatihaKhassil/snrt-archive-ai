import asyncio
import json
import time

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from prometheus_client import start_http_server

from tika_service import TikaService
from document_repository import DocumentRepository

from kafka_producer import kafka_producer
from topics import (
    DOCUMENT_UPLOADED,
    TEXT_EXTRACTED
)

from metrics import (
    documents_received_total,
    documents_processed_total,
    documents_success_total,
    documents_failed_total,
    documents_processing,
    extraction_duration,
    worker_errors_total
)


KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC = DOCUMENT_UPLOADED


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
                group_id="snrt-document-worker-v1",
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
                "📄 Document Worker started...",
                flush=True
            )

            print(
                "Waiting for documents...",
                flush=True
            )

            return consumer

        except KafkaConnectionError as e:

            print(
                f"⏳ Kafka not ready: {e}",
                flush=True
            )

            worker_errors_total.labels(
                worker="document-worker"
            ).inc()

            if consumer:

                await consumer.stop()

            await asyncio.sleep(5)


async def consume():

    tika_service = TikaService()

    repository = DocumentRepository()

    consumer = await create_consumer()

    await kafka_producer.start()

    try:

        async for message in consumer:

            print(
                "\n📩 Message received from Kafka",
                flush=True
            )

            documents_received_total.inc()

            documents_processing.inc()

            try:

                data = json.loads(
                    message.value.decode("utf-8")
                )

                document_id = data.get(
                    "document_id"
                )

                file_type = data.get(
                    "file_type"
                )

                file_path = data.get(
                    "storage_path"
                )

                print(
                    "==========================",
                    flush=True
                )

                print(
                    "📄 New document received",
                    flush=True
                )

                print(
                    "==========================",
                    flush=True
                )

                print(
                    "Document ID :",
                    document_id,
                    flush=True
                )

                print(
                    "File type :",
                    file_type,
                    flush=True
                )

                print(
                    "Path :",
                    file_path,
                    flush=True
                )

                # ====================================================
                # AUDIO DOCUMENT
                # ====================================================

                if file_type == "audio":

                    print(
                        "⏭ Audio detected, skipping...",
                        flush=True
                    )

                    continue

                # ====================================================
                # TEXT EXTRACTION
                # ====================================================

                print(
                    "📑 Starting text extraction...",
                    flush=True
                )

                extraction_start = time.perf_counter()

                try:

                    extracted_text = await asyncio.to_thread(
                        tika_service.extract,
                        file_path
                    )

                    extraction_time = (
                        time.perf_counter()
                        - extraction_start
                    )

                    extraction_duration.observe(
                        extraction_time
                    )

                    print(
                        f"⏱️ Extraction duration: "
                        f"{extraction_time:.2f}s",
                        flush=True
                    )

                except Exception as e:

                    documents_failed_total.inc()

                    worker_errors_total.labels(
                        worker="document-worker"
                    ).inc()

                    print(
                        f"❌ Tika extraction error: {e}",
                        flush=True
                    )

                    continue

                print(
                    "✅ Extraction completed",
                    flush=True
                )

                # ====================================================
                # SAVE TO MONGODB
                # ====================================================

                try:

                    await repository.update_extracted_text(
                        document_id,
                        extracted_text
                    )

                    print(
                        "✅ Text saved to MongoDB",
                        flush=True
                    )

                except Exception as e:

                    documents_failed_total.inc()

                    worker_errors_total.labels(
                        worker="document-worker"
                    ).inc()

                    print(
                        f"❌ MongoDB error: {e}",
                        flush=True
                    )

                    continue

                # ====================================================
                # SEND TO KAFKA
                # ====================================================

                try:

                    print(
                        "📤 Sending extracted text to Kafka...",
                        flush=True
                    )

                    await kafka_producer.send(
                        TEXT_EXTRACTED,
                        {
                            "document_id": document_id,
                            "text": extracted_text
                        }
                    )

                    print(
                        "✅ Text sent to Kafka",
                        flush=True
                    )

                except Exception as e:

                    documents_failed_total.inc()

                    worker_errors_total.labels(
                        worker="document-worker"
                    ).inc()

                    print(
                        f"❌ Kafka error: {e}",
                        flush=True
                    )

                    continue

                # ====================================================
                # SUCCESS
                # ====================================================

                documents_processed_total.inc()

                documents_success_total.inc()

                print(
                    "✅ Document processed successfully",
                    flush=True
                )

                print(
                    "==========================",
                    flush=True
                )

            except Exception as e:

                documents_failed_total.inc()

                worker_errors_total.labels(
                    worker="document-worker"
                ).inc()

                print(
                    f"❌ Unexpected worker error: {e}",
                    flush=True
                )

            finally:

                documents_processing.dec()

    finally:

        await kafka_producer.stop()

        await consumer.stop()

        print(
            "🛑 Document Worker stopped",
            flush=True
        )


if __name__ == "__main__":

    start_http_server(8000)

    print(
        "📊 Prometheus metrics available on port 8000",
        flush=True
    )

    asyncio.run(
        consume()
    )