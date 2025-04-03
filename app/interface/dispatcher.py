from celery.result import AsyncResult
from app.core.celery_app import celery_app


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
        # Using send_task with exact task name instead of importing the task
        return celery_app.send_task("execute_quantum_circuit", args=[qasm_str])

    def execute_dummy_task(self, qasm_str: str):
        """
        Dispatches a dummy task (for backward compatibility)
        Returns the celery task object
        """
        return celery_app.send_task("execute_dummy_circuit", args=[qasm_str])

    def get_task_result(self, task_id: str):
        """
        Retrieves the result of a task by its ID with debug info
        """
        task = AsyncResult(task_id, app=celery_app)

        # Add debug info
        debug_info = {
            "task_id": task_id,
            "state": task.state,
            "ready": task.ready(),
            "successful": task.successful() if task.ready() else None,
        }

        try:
            if task.result:
                debug_info["result"] = task.result
        except:
            debug_info["result_error"] = "Could not access result"

        # Return all info for debugging
        return {
            "status": task.state.lower(),
            "debug": debug_info,
            "message": f"Task is in state: {task.state}",
            "result": task.result if task.ready() and task.successful() else None
        }


# Create a singleton dispatcher instance
dispatcher = CircuitTaskDispatcher()
