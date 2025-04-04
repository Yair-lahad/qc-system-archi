from fastapi import APIRouter, HTTPException
from app.core.models import TaskRequest, TaskResponse, TaskStatusResponse
from app.interface.dispatcher import dispatcher

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse)
async def create_task(payload: TaskRequest):
    task = await dispatcher.execute_circuit(payload.qc)
    return TaskResponse(task_id=task.id, message="Task submitted successfully.")


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task(task_id: str):
    result_data = await dispatcher.get_task_result(task_id)

    if result_data["status"] == "error":
        raise HTTPException(status_code=404, detail=result_data["message"])

    return TaskStatusResponse(**result_data)
