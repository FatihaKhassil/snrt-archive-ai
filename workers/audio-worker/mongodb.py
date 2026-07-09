from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URL = "mongodb://mongodb:27017"

DATABASE_NAME = "snrt_archive"


client = AsyncIOMotorClient(MONGO_URL)

database = client[DATABASE_NAME]

documents_collection = database["documents"]