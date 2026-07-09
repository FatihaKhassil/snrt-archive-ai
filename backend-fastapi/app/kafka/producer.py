import json

from aiokafka import AIOKafkaProducer

from app.core.config import settings


class KafkaProducerService:

    def __init__(self):
        self.producer = None

    async def start(self):

        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
        )

        await self.producer.start()

    async def stop(self):

        if self.producer is not None:
            await self.producer.stop()

    async def send(self, topic: str, message: dict):

        if self.producer is None:
            raise RuntimeError("Kafka Producer is not started.")

        await self.producer.send_and_wait(
            topic,
            json.dumps(message).encode("utf-8")
        )


kafka_producer = KafkaProducerService()