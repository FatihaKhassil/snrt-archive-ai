import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from whisper_service import WhisperService
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

            if consumer:
                await consumer.stop()

            await asyncio.sleep(5)



async def consume():

    # Chargement du modèle Whisper
    whisper_service = WhisperService()

    # Repository MongoDB
    document_repository = DocumentRepository()


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


            print(
                "==========================",
                flush=True
            )

            print(
                "📄 New document received",
                flush=True
            )


            document_id = data.get("document_id")
            file_type = data.get("file_type")
            audio_path = data.get("storage_path")


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
                audio_path,
                flush=True
            )


            if file_type == "audio":

                print(
                    "🎤 Starting transcription...",
                    flush=True
                )


                text = whisper_service.transcribe(
                    audio_path
                )


                print(
                    "📝 Transcription :",
                    text,
                    flush=True
                )


                # Sauvegarde dans MongoDB
                await document_repository.update_transcription(
                    document_id,
                    text
                )


                print(
                    "✅ Transcription saved to MongoDB",
                    flush=True
                )


            print(
                "==========================",
                flush=True
            )


    finally:

        await consumer.stop()

        print(
            "🛑 Audio Worker stopped",
            flush=True
        )



if __name__ == "__main__":

    asyncio.run(consume())