import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from kafka_producer import kafka_producer
from topics import (
    TEXT_EXTRACTED,
    LLM_COMPLETED
)

from llm_service import LLMService
from document_repository import DocumentRepository


KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC = TEXT_EXTRACTED


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

            if consumer:
                await consumer.stop()

            await asyncio.sleep(5)


async def consume():

    llm_service = LLMService()

    repository = DocumentRepository()

    consumer = await create_consumer()

    await kafka_producer.start()

    try:

        async for message in consumer:

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

            result = await asyncio.to_thread(

                llm_service.process,

                text

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

    finally:

        await kafka_producer.stop()

        await consumer.stop()

        print(
            "🛑 LLM Worker stopped",
            flush=True
        )


if __name__ == "__main__":

    asyncio.run(
        consume()
    )