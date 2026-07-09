import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError


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


            print("==========================", flush=True)

            print(
                "📄 New document received",
                flush=True
            )

            print(
                "Document ID :",
                data.get("document_id"),
                flush=True
            )

            print(
                "File type :",
                data.get("file_type"),
                flush=True
            )

            print(
                "Path :",
                data.get("storage_path"),
                flush=True
            )

            print("==========================", flush=True)


    finally:

        await consumer.stop()

        print(
            "🛑 Audio Worker stopped",
            flush=True
        )



if __name__ == "__main__":

    asyncio.run(consume())