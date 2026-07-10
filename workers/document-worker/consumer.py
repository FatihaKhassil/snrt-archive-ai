import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from tika_service import TikaService
from document_repository import DocumentRepository


KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC = "document-uploaded"


async def create_consumer():

    while True:

        consumer = None

        try:

            print("⏳ Connecting to Kafka...", flush=True)

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

            if consumer:
                await consumer.stop()

            await asyncio.sleep(5)


async def consume():

    tika_service = TikaService()

    repository = DocumentRepository()

    consumer = await create_consumer()

    try:

        async for message in consumer:

            print(
                "\n📩 Message received from Kafka",
                flush=True
            )

            data = json.loads(
                message.value.decode("utf-8")
            )

            document_id = data.get("document_id")
            file_type = data.get("file_type")
            file_path = data.get("storage_path")

            print("==========================")
            print("📄 New document received")
            print("==========================")
            print("Document ID :", document_id)
            print("File type :", file_type)
            print("Path :", file_path)

            # Les fichiers audio sont traités par audio-worker
            if file_type == "audio":

                print(
                    "⏭ Audio detected, skipping...",
                    flush=True
                )

                continue

            print(
                "📑 Starting text extraction...",
                flush=True
            )

            extracted_text = tika_service.extract(
                file_path
            )

            print(
                "✅ Extraction completed",
                flush=True
            )

            await repository.update_extracted_text(
                document_id,
                extracted_text
            )

            print(
                "✅ Text saved to MongoDB",
                flush=True
            )

    finally:

        await consumer.stop()

        print(
            "🛑 Document Worker stopped",
            flush=True
        )


if __name__ == "__main__":

    asyncio.run(consume())