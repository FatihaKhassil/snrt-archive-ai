from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.upload import router as upload_router
from app.api.search import router as search_router
from app.api.rag import router as rag_router
from app.api.documents import router as documents_router
from app.api.users import router as users_router
from app.api.auth import router as auth_router

from app.core.config import settings
from app.database.mongodb import client
from app.kafka.producer import kafka_producer
from app.api.dashboard import router as dashboard_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)
Instrumentator().instrument(app).expose(app)

# ==========================
# CORS Configuration
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================
# Startup
# ==========================

@app.on_event("startup")
async def startup():

    try:

        await client.admin.command("ping")
        print("✅ MongoDB Connected Successfully")

        await kafka_producer.start()
        print("✅ Kafka Connected Successfully")

    except Exception as e:

        print(e)


# ==========================
# Routes
# ==========================

app.include_router(upload_router)
app.include_router(search_router)
app.include_router(rag_router)
app.include_router(documents_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(dashboard_router)


@app.get("/")
def root():

    return {

        "message": settings.APP_NAME

    }


# ==========================
# Shutdown
# ==========================

@app.on_event("shutdown")
async def shutdown():

    await kafka_producer.stop()

    print("✅ Kafka Connection Closed")