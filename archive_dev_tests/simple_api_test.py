from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

# simple_api File is used to check if FASTAPI works in his UI example at localhost:8000/docs.

app = FastAPI()

task_store = {}

class TaskRequest(BaseModel):
    qc: str

@app.post("/tasks")
def create_task(payload: TaskRequest):
    task_id = str(uuid.uuid4())
    # Simulate background job submission
    task_store[task_id] = {
        "status": "pending",
        "result": None,
        "input": payload.qc
    }
    return {"task_id": task_id, "message": "Task received."}

@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Simulate that after a few seconds, result becomes available
    task["status"] = "completed"
    task["result"] = {"message": "Simulated result", "input": task['input']}
    return task
