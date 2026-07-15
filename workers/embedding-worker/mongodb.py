from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient(
    "mongodb://mongodb:27017"
)

mongodb = client["snrt_archive"]