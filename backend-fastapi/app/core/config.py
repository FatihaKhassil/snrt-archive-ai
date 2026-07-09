import os

class Settings:

    APP_NAME = os.getenv("APP_NAME")

    APP_VERSION = os.getenv("APP_VERSION")

    MONGO_HOST = os.getenv("MONGO_HOST")

    MONGO_PORT = os.getenv("MONGO_PORT")

    MONGO_DB = os.getenv("MONGO_DB")

    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

    KAFKA_DOCUMENT_TOPIC = os.getenv("KAFKA_DOCUMENT_TOPIC")

    KAFKA_TRANSCRIPTION_TOPIC = os.getenv("KAFKA_TRANSCRIPTION_TOPIC")

    KAFKA_LLM_TOPIC = os.getenv("KAFKA_LLM_TOPIC")


settings = Settings()