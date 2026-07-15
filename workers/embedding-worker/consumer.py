import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from kafka_producer import kafka_producer
from topics import (
    LLM_COMPLETED
)

from document_repository import DocumentRepository
from services.text_splitter import TextSplitter
from chroma_service import ChromaService


KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC = LLM_COMPLETED


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

            if consumer:

                await consumer.stop()

            await asyncio.sleep(5)


async def consume():

    repository = DocumentRepository()

    splitter = TextSplitter()

    chroma = ChromaService()

    consumer = await create_consumer()

    await kafka_producer.start()

    try:

        async for message in consumer:

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

            print(
                "📄 Loading transcription...",
                flush=True
            )

            transcription = await repository.get_transcription(

                document_id

            )

            if not transcription:

                print(
                    "❌ Transcription not found",
                    flush=True
                )

                continue

            print(
                "✂ Splitting text...",
                flush=True
            )

            chunks = splitter.split(

                transcription

            )

            print(
                f"✅ {len(chunks)} chunks created",
                flush=True
            )

            print(
                "📦 Storing chunks into ChromaDB...",
                flush=True
            )

            await asyncio.to_thread(

                chroma.add_document,

                document_id,

                chunks

            )

            print(
                "✅ Chunks stored",
                flush=True
            )
            count = chroma.count_documents()

            print(
                f"📊 Total chunks in Chroma : {count}",
                flush=True
            )

            await repository.update_embedding_status(

                document_id

            )

            print(
                "✅ MongoDB updated",
                flush=True
            )

    finally:

        await kafka_producer.stop()

        await consumer.stop()

        print(
            "🛑 Embedding Worker stopped",
            flush=True
        )


if __name__ == "__main__":

    asyncio.run(

        consume()

    )