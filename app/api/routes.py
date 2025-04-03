from fastapi import APIRouter, HTTPException
from app.core.models import TaskRequest, TaskResponse, TaskStatusResponse
from app.interface.dispatcher import dispatcher

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse)
def create_task(payload: TaskRequest):
    """Submit a quantum circuit for execution"""
    task = dispatcher.execute_circuit(payload.qc)
    return TaskResponse(task_id=task.id, message="Task submitted successfully.")


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
def get_task(task_id: str):
    """Get the status and result of a submitted task"""
    result = dispatcher.get_task_result(task_id)

    if result.state == 'PENDING':
        return TaskStatusResponse(
            status="pending",
            message="Task is still in progress."
        )
    elif result.state == 'SUCCESS':
        return TaskStatusResponse(
            status="completed",
            result=result.result
        )
    elif result.state == 'FAILURE':
        return TaskStatusResponse(
            status="error",
            message=str(result.result)
        )
    else:
        raise HTTPException(status_code=404, detail="Task not found.")
