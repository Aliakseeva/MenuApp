from celery import Celery

from MenuApp.src.db.config import settings

celery = Celery(
    "tasks",
    broker=settings.BROKER_URL,
    backend=settings.BACKEND_URL,
    include=["MenuApp.src.services.tasks.report"],
)
