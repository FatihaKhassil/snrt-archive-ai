import asyncio
import json

from aiokafka import AIOKafkaProducer

from app.core.config import settings


class KafkaProducerService:

    def __init__(self):
        self.producer = None

    async def start(self):

        print("⏳ Starting Kafka Producer...", flush=True)

        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
        )

        await self.producer.start()

        print("✅ Kafka Producer started", flush=True)

    async def stop(self):

        if self.producer is not None:

            await self.producer.stop()

            print("🛑 Kafka Producer stopped", flush=True)

    async def send(self, topic: str, message: dict):

        if self.producer is None:
            raise RuntimeError(
                "Kafka Producer is not started."
            )

        print(
            "====================================",
            flush=True
        )

        print(
            "📤 Sending message to Kafka...",
            flush=True
        )

        print(
            f"Topic : {topic}",
            flush=True
        )

        print(
            f"Message : {message}",
            flush=True
        )

        print(
            "====================================",
            flush=True
        )

        try:

            metadata = await asyncio.wait_for(

                self.producer.send_and_wait(

                    topic,

                    json.dumps(
                        message
                    ).encode("utf-8")

                ),

                timeout=10

            )

            print(
                "====================================",
                flush=True
            )

            print(
                "✅ Kafka ACK received",
                flush=True
            )

            print(
                f"Topic     : {metadata.topic}",
                flush=True
            )

            print(
                f"Partition : {metadata.partition}",
                flush=True
            )

            print(
                f"Offset    : {metadata.offset}",
                flush=True
            )

            print(
                "====================================",
                flush=True
            )

            return True

        except asyncio.TimeoutError:

            print(
                "====================================",
                flush=True
            )

            print(
                "⚠️ Kafka timeout after 10 seconds",
                flush=True
            )

            print(
                "====================================",
                flush=True
            )

            return False

        except Exception as e:

            print(
                "====================================",
                flush=True
            )

            print(
                "❌ ERROR while sending message to Kafka",
                flush=True
            )

            print(
                type(e).__name__,
                flush=True
            )

            print(
                str(e),
                flush=True
            )

            print(
                "====================================",
                flush=True
            )

            return False


kafka_producer = KafkaProducerService()