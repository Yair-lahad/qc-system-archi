import logging
import time
from app.core.celery_app import celery_app
from app.core.redis_client import get_redis_client

print("Task module loaded.")
logger = logging.getLogger("worker")


def execute_quantum_circuit(qc_string):
    """
    Execute a quantum circuit from its QASM string representation

    This contains the core business logic for quantum circuit execution
    without any dependency on Celery.
    """
    print("STEP 1: inside execute_quantum_circuit")
    logger.info("STEP 1")

    time.sleep(1)

    try:
        print("STEP 2: getting Redis client")
        redis = get_redis_client()
        print("STEP 3: calling redis.incr()")
        redis.incr('stats:completed_tasks')
        print("STEP 4: redis.incr() succeeded")
    except Exception as e:
        print("STEP ERR: failed to get redis or incr")
        logger.warning(f"Could not update metrics: {str(e)}")

    print("STEP 5: returning result")
    return {"message": "Circuit executed successfully", "input": qc_string}

# Register the task with the exact name used in dispatcher.py


@celery_app.task
def execute_circuit_task(qasm_str):
    """
    Execute a quantum circuit from its QASM string
    """
    print("TASK: Received input:", qasm_str)
    return execute_quantum_circuit(qasm_str)


@celery_app.task(name='add')
def add(x, y):
    return x + y
