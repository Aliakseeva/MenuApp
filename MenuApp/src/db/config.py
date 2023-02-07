import os

from dotenv import load_dotenv

from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    DB_HOST = os.environ.get("URL_DB")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("POSTGRES_DB")
    DB_USER = os.environ.get("POSTGRES_USER")
    DB_PASS = os.environ.get("POSTGRES_PASSWORD")

    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = os.environ.get("REDIS_PORT")
    REDIS_DB = os.environ.get("REDIS_DB")

    CACHE_REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

    RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
    RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT")
    RABBITMQ_DEFAULT_USER = os.environ.get("RABBITMQ_DEFAULT_USER")
    RABBITMQ_DEFAULT_PASS = os.environ.get("RABBITMQ_DEFAULT_PASS")

    BROKER_URL = f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}//"
    BACKEND_URL = 'rpc://'


settings = Settings()
