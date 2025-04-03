from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from app.workers.circuit_executor import dummy_task  # import actual function
from app.core.celery_app import celery_app

# Routes uses FastAPI which acts as Receptionist with 3 funcionalities:

# Takes requests from clients.
# Forward tickets of tasks to the workers (Celery)
# Return messages to clients.

router = APIRouter()


class TaskRequest(BaseModel):  # Object for Quantum Circuit
    qc: str


@router.post("/tasks")
def create_task(payload: TaskRequest):
    task = dummy_task.delay(payload.qc)
    return {"task_id": task.id, "message": "Task submitted successfully."}


@router.get("/tasks/{task_id}")
def get_task(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.state == 'PENDING':
        return {"status": "pending", "message": "Task is still in progress."}
    elif result.state == 'SUCCESS':
        return {"status": "completed", "result": result.result}
    elif result.state == 'FAILURE':
        return {"status": "error", "message": str(result.result)}
    else:
        raise HTTPException(status_code=404, detail="Task not found.")
