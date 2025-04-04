from celery import Celery
import logging
from app.core.config import BROKER_URL, RESULT_BACKEND

logger = logging.getLogger("api")

# Celery is Task Queue library.
# Helps to send and receive messages via "Message Broker", making sure they are not lost.
# Keeps consistency and maintainability across the project.
# Our Message Broker is Redis, making the Async proccessing by itself.
# Modularity is used here, we can easily switch a Broker.

logger.info(f"Configuring Celery with broker: {BROKER_URL}")

# Creates an Instance of the Celery application.
celery_app = Celery(
    "quantum_tasks",
    broker=BROKER_URL,
    backend=RESULT_BACKEND
)

# Ensure task modules are imported and registered with Celery
celery_app.conf.imports = [
    'app.workers.tasks',
]

# Optional: Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    task_track_started=True,
    worker_prefetch_multiplier=1,
)
