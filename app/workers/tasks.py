import logging
import time
from app.core.celery_app import celery_app
from app.core.redis_client import get_redis_client

logger = logging.getLogger("worker")


def execute_quantum_circuit(qc_string):
    """
    Execute a quantum circuit from its QASM string representation

    This contains the core business logic for quantum circuit execution
    without any dependency on Celery.
    """
    logger.info(f"Executing quantum circuit")
    # In a real implementation, this would parse the QASM and execute on a simulator or real quantum device
    time.sleep(2)  # Simulating processing time

    # Record basic execution metrics
    try:
        redis = get_redis_client()
        redis.incr('stats:completed_tasks')
    except Exception as e:
        logger.warning(f"Could not update metrics: {str(e)}")

    return {"message": "Circuit executed successfully", "input": qc_string}

# Register the task with the exact name used in dispatcher.py


@celery_app.task
def execute_circuit_task(qasm_str):
    """
    Execute a quantum circuit from its QASM string
    """
    return execute_quantum_circuit(qasm_str)
