from celery import Celery
import os

# Celery is Task Queue library.
# Helps to send and receive messages via "Message Broker", making sure they are not lost.
# Keeps consistency and maintainability across the project.
# Our Message Broker is Redis, making the Async proccessing by itself.
# Modularity is used here, we can easily switch a Broker.

# read more at https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html


BROKER_URL = "redis://localhost:6379/0"
RESULT_BACKEND = "redis://localhost:6379/0"
# BROKER_URL = os.getenv("LOCAL_URL", "redis://redis:6379/0")
# RESULT_BACKEND = os.getenv("LOCAL_BACKEND", "redis://redis:6379/0")

# Initialize Celery with proper configuration
celery_app = Celery(
    "quantum_tasks",
    broker=BROKER_URL,
    backend=RESULT_BACKEND
)

# Add configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Include the task modules explicitly
celery_app.conf.task_routes = {
    'execute_quantum_circuit': {'queue': 'default'},
    'execute_dummy_circuit': {'queue': 'default'},
}

# Auto-discover tasks
celery_app.autodiscover_tasks(['app.workers'])
