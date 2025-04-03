from fastapi import FastAPI
from app.api import tasks

app = FastAPI()
app.include_router(tasks.router)

# app/api/tasks.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from app.core.celery_app import celery_app

router = APIRouter()

class TaskRequest(BaseModel):
    qc: str

@router.post("/tasks")
def create_task(payload: TaskRequest):
    task = celery_app.send_task("workers.circuit_executor.dummy_task", args=[payload.qc])
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
        raise HTTPException(status_code=404, detail="Task not found")
