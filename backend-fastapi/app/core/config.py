import os

class Settings:

    APP_NAME = os.getenv("APP_NAME")

    APP_VERSION = os.getenv("APP_VERSION")

    MONGO_HOST = os.getenv("MONGO_HOST")

    MONGO_PORT = os.getenv("MONGO_PORT")

    MONGO_DB = os.getenv("MONGO_DB")


settings = Settings()