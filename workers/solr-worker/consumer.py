import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from topics import (
    LLM_COMPLETED
)

from document_repository import DocumentRepository
from solr_service import SolrService


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

            if consumer:

                await consumer.stop()

            await asyncio.sleep(5)


async def consume():

    repository = DocumentRepository()

    solr = SolrService()

    consumer = await create_consumer()

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
                "📄 Loading document from MongoDB...",
                flush=True
            )

            document = await repository.get_document(

                document_id

            )

            if not document:

                print(
                    "❌ Document not found",
                    flush=True
                )

                continue

            print(
                "📦 Sending document to Solr...",
                flush=True
            )

            solr_document = {

                "id": str(document["_id"]),

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

            await asyncio.to_thread(

                solr.index_document,

                solr_document

            )

            print(
                "✅ Document indexed in Solr",
                flush=True
            )

            await repository.update_solr_status(

                document_id

            )

            print(
                "✅ MongoDB updated",
                flush=True
            )

    finally:

        await consumer.stop()

        print(
            "🛑 Solr Worker stopped",
            flush=True
        )


if __name__ == "__main__":

    asyncio.run(

        consume()

    )