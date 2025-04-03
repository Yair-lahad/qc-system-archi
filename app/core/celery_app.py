from celery import Celery
import os

# BROKER_URL = os.getenv("LOCAL_URL", "redis://redis:6379/0")
# RESULT_BACKEND = os.getenv("LOCAL_BACKEND", "redis://redis:6379/0")

BROKER_URL = "redis://localhost:6379/0"
RESULT_BACKEND = "redis://localhost:6379/0"


# Celery is Task Queue library.
# it helps to send and receive messages via "Message Broker", making sure they are not lost.
# Our Message Broker is Redis, making the Async proccessing by itself.
# Modularity is used here, we can easily switch a Broker.

# read more at https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html

celery_app = Celery(
    "quantum_tasks",
    broker=BROKER_URL,
    backend=RESULT_BACKEND
)
