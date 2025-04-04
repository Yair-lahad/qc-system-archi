"""
routes.py - FastAPI routes for quantum task submission and status retrieval.

Exposes endpoints to:
- Submit a quantum task with QASM3 input
- Retrieve result by task ID
- Provide a healthcheck ping
"""
from fastapi import APIRouter, HTTPException
from app.core.models import TaskRequest, TaskResponse, TaskStatusResponse
from app.interface.dispatcher import dispatcher

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse)
async def create_task(payload: TaskRequest):
    """
    Submit a QASM3 quantum circuit for async execution.
    Args:
        request (TaskRequest): Contains the quantum circuit as a string in 'qc'.
    Returns:
        TaskResponse: Contains task ID and confirmation message.
    Raises:
        HTTPException: If dispatcher validation fails.
    """
    try:
        task = await dispatcher.execute_circuit(payload.qc)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return TaskResponse(task_id=task.id, message="Task submitted successfully.")


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse, response_model_exclude_none=True)
async def get_task(task_id: str):
    """
    Retrieve result or status of a submitted quantum task.
    Args:
        task_id (str): ID of the Celery task.
    Returns:
        TaskStatusResponse: Includes task status and result/message.
    """
    result_data = await dispatcher.get_task_result(task_id)
    if result_data["status"] == "error":
        raise HTTPException(status_code=404, detail=result_data["message"])

    return TaskStatusResponse(**result_data)


@router.get("/health/ping")
def ping():
    """
    Lightweight API healthcheck endpoint.
    Returns:
        dict: Status indicating the API is reachable.
    """
    return {"status": "ok"}
