from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

print("HOST =", settings.MONGO_HOST)
print("PORT =", settings.MONGO_PORT)
print("DB =", settings.MONGO_DB)

MONGO_URL = f"mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}"

print(MONGO_URL)

client = AsyncIOMotorClient(MONGO_URL)

database = client[settings.MONGO_DB]