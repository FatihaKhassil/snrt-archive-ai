import asyncio
import json
import time

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from prometheus_client import start_http_server

from whisper_service import WhisperService
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
    transcription_duration,
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
                group_id="snrt-audio-worker-v1",
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
                "🎧 Audio Worker started...",
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
                worker="audio-worker"
            ).inc()

            if consumer:

                await consumer.stop()

            await asyncio.sleep(5)


async def consume():

    whisper_service = WhisperService()

    document_repository = DocumentRepository()

    consumer = await create_consumer()

    await kafka_producer.start()

    try:

        async for message in consumer:

            print(
                "\n📩 Message received from Kafka",
                flush=True
            )

            try:

                data = json.loads(
                    message.value.decode("utf-8")
                )

                print(
                    "==========================",
                    flush=True
                )

                print(
                    "📄 New document received",
                    flush=True
                )

                document_id = data.get(
                    "document_id"
                )

                document_type = data.get(
                    "document_type"
                )

                file_type = data.get(
                    "file_type"
                )

                audio_path = data.get(
                    "storage_path"
                )

                print(
                    "Document ID :",
                    document_id,
                    flush=True
                )

                print(
                    "Document type :",
                    document_type,
                    flush=True
                )

                print(
                    "File type :",
                    file_type,
                    flush=True
                )

                print(
                    "Path :",
                    audio_path,
                    flush=True
                )

                if document_type != "audio":

                    print(
                        "⏭ Not an audio document, skipping...",
                        flush=True
                    )

                    continue

                # ====================================================
                # DOCUMENT RECEIVED
                # ====================================================

                documents_received_total.inc()

                documents_processing.inc()

                print(
                    "🎤 Starting transcription...",
                    flush=True
                )

                # ====================================================
                # TRANSCRIPTION
                # ====================================================

                transcription_start = time.perf_counter()

                try:

                    text = await asyncio.to_thread(
                        whisper_service.transcribe,
                        audio_path
                    )

                    transcription_time = (
                        time.perf_counter()
                        - transcription_start
                    )

                    transcription_duration.observe(
                        transcription_time
                    )

                    print(
                        f"⏱️ Transcription duration: "
                        f"{transcription_time:.2f}s",
                        flush=True
                    )

                except Exception as e:

                    documents_failed_total.inc()

                    worker_errors_total.labels(
                        worker="audio-worker"
                    ).inc()

                    print(
                        f"❌ Transcription error: {e}",
                        flush=True
                    )

                    continue

                print(
                    "📝 Transcription :",
                    text,
                    flush=True
                )

                # ====================================================
                # SAVE TRANSCRIPTION IN MONGODB
                # ====================================================

                try:

                    await document_repository.update_transcription(
                        document_id,
                        text
                    )

                    print(
                        "✅ Transcription saved to MongoDB",
                        flush=True
                    )

                except Exception as e:

                    documents_failed_total.inc()

                    worker_errors_total.labels(
                        worker="audio-worker"
                    ).inc()

                    print(
                        f"❌ MongoDB error: {e}",
                        flush=True
                    )

                    continue

                # ====================================================
                # SEND TEXT TO KAFKA
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
                            "text": text
                        }
                    )

                    print(
                        "✅ Text sent to Kafka",
                        flush=True
                    )

                except Exception as e:

                    documents_failed_total.inc()

                    worker_errors_total.labels(
                        worker="audio-worker"
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
                    "✅ Audio document processed successfully",
                    flush=True
                )

                print(
                    "==========================",
                    flush=True
                )

            except Exception as e:

                documents_failed_total.inc()

                worker_errors_total.labels(
                    worker="audio-worker"
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
            "🛑 Audio Worker stopped",
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