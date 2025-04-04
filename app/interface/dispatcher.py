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

    def execute_circuit(self, qasm_str: str):
        """
        Dispatches a quantum circuit execution task
        """
        return celery_app.send_task("app.workers.tasks.execute_circuit_task", args=[qasm_str])

    def get_task_result(self, task_id: str):
        """
        Retrieves the result of a task by its ID.

        This method provides a clean interface for checking task status and
        getting results, abstracting away the details of the Celery backend.

        Args:
            task_id: The unique identifier of the task

        Returns:
            Celery AsyncResult object containing task status and result
        """
        logger.debug(f"Retrieving result for task ID: {task_id}")
        return AsyncResult(task_id, app=celery_app)


# Create a singleton dispatcher instance for use throughout the application
dispatcher = CircuitTaskDispatcher()
