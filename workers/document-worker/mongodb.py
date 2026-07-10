from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient(
    "mongodb://mongodb:27017"
)


database = client["snrt_archive"]


documents_collection = database["documents"]