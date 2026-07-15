from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.search import router as search_router

from app.core.config import settings
from app.database.mongodb import client
from app.kafka.producer import kafka_producer


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)


@app.on_event("startup")
async def startup():

    try:

        await client.admin.command("ping")
        print("✅ MongoDB Connected Successfully")

        await kafka_producer.start()
        print("✅ Kafka Connected Successfully")

    except Exception as e:

        print(e)


app.include_router(upload_router)
app.include_router(search_router)


@app.get("/")
def root():

    return {

        "message": settings.APP_NAME

    }


@app.on_event("shutdown")
async def shutdown():

    await kafka_producer.stop()

    print("✅ Kafka Connection Closed")