from app.core.celery_app import celery_app
import time

@celery_app.task(name="workers.circuit_executor.dummy_task")
def dummy_task(qc_string):
    time.sleep(2)
    return {"message": "Executed dummy task", "input": qc_string}
