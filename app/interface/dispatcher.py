from core.celery_app import celery_app
from workers.circuit_executor import dummy_task  # or execute_circuit, etc.

@celery.task(name="execute_circuit")
def create_task(qasm3_str: str) -> str:
    task = dummy_task.delay(qasm3_str)
    return task.id
