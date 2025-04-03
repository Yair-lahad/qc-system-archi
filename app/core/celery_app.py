from celery import Celery
import os

BROKER_URL = os.getenv("BROKER_URL", "redis://redis:6379/0")
RESULT_BACKEND = os.getenv("RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery(
    "quantum_tasks",
    broker=BROKER_URL,
    backend=RESULT_BACKEND
)