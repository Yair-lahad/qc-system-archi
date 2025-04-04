from celery.result import AsyncResult
from app.core.celery_app import celery_app
import logging

logger = logging.getLogger("api")


class CircuitTaskDispatcher:
    """
    Interface layer between API endpoints and worker tasks.

    The dispatcher serves multiple important purposes in the architecture:

    1. Separation of concerns:
       - Abstracts away task submission and retrieval details from API code
       - Keeps API routes focused on HTTP request/response handling
       - Allows worker code to focus on task execution logic

    2. Encapsulation of task management:
       - Centralizes how tasks are dispatched and monitored
       - Makes it easier to modify task processing behavior in one place
       - Simplifies potential future changes to the task queue system

    3. Provides a consistent interface:
       - API code can interact with tasks through a clean, consistent API
       - Makes the codebase more maintainable as it grows
       - Enables centralized logging and metrics collection
    """

    async def execute_circuit(self, qasm_str: str):
        """
        Dispatches a quantum circuit execution task
        """
        return celery_app.send_task("app.workers.tasks.execute_circuit_task", args=[qasm_str])

    async def get_task_result(self, task_id: str):
        """
        Retrieves the result of a task by its ID, and returns a JSON-friendly dict.
        """
        logger.debug(f"Retrieving result for task ID: {task_id}")
        result = AsyncResult(task_id, app=celery_app)

        if result.successful():
            return {
                "status": "completed",
                "result": result.result
            }
        elif result.state in ("PENDING", "RECEIVED", "STARTED"):
            return {
                "status": "pending",
                "message": "Task is still in progress."
            }
        else:
            return {
                "status": "error",
                "message": "Task not found or failed."
            }


# Create a singleton dispatcher instance for use throughout the application
dispatcher = CircuitTaskDispatcher()
