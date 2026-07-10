from motor.motor_asyncio import AsyncIOMotorClient


class MongoDB:

    def __init__(self):

        self.client = AsyncIOMotorClient(
            "mongodb://mongodb:27017"
        )

        self.database = self.client["snrt_archive"]

        self.documents = self.database["documents"]


mongodb = MongoDB()