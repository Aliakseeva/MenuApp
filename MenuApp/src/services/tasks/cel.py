from celery import Celery

from MenuApp.src.config import (
    RABBITMQ_DEFAULT_PASS,
    RABBITMQ_DEFAULT_USER,
    RABBITMQ_HOST,
)

celery = Celery(
    "cel",
    broker=f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}//",
    backend="rpc://",
    include=["MenuApp.src.services.tasks.report"],
)
