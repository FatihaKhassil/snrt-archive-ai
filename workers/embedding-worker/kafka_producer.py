import json

from aiokafka import AIOKafkaProducer


class KafkaProducer:

    def __init__(self):

        self.producer = None


    async def start(self):

        self.producer = AIOKafkaProducer(

            bootstrap_servers="kafka:9092"

        )

        await self.producer.start()


    async def stop(self):

        if self.producer:

            await self.producer.stop()


    async def send(

        self,

        topic,

        message

    ):

        await self.producer.send_and_wait(

            topic,

            json.dumps(message).encode("utf-8")

        )


kafka_producer = KafkaProducer()