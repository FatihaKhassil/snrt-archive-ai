from fastapi import FastAPI

from app.core.config import settings
from app.database.mongodb import client

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)


@app.on_event("startup")
async def startup():

    try:
        await client.admin.command("ping")
        print("✅ MongoDB Connected Successfully")

    except Exception as e:
        print(e)


@app.get("/")
def root():

    return {
        "message": settings.APP_NAME
    }