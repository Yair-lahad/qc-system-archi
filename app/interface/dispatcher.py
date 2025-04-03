from celery.result import AsyncResult
from app.core.celery_app import celery_app
from app.workers.task_registry import execute_circuit_task, dummy_task


class CircuitTaskDispatcher:
    """
    Interface layer between API and worker tasks

    Responsible for dispatching circuit execution tasks and retrieving results
    """

    def execute_circuit(self, qasm_str: str):
        """
        Dispatches a quantum circuit execution task
        Returns the celery task object
        """
        return execute_circuit_task.delay(qasm_str)

    def execute_dummy_task(self, qasm_str: str):
        """
        Dispatches a dummy task (for backward compatibility)
        Returns the celery task object
        """
        return dummy_task.delay(qasm_str)

    def get_task_result(self, task_id: str):
        """
        Retrieves the result of a task by its ID
        """
        return AsyncResult(task_id, app=celery_app)


# Create a singleton dispatcher instance
dispatcher = CircuitTaskDispatcher()
