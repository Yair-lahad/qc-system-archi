from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class TaskRequest(BaseModel):
    """
    Data model representing a quantum circuit task request
    """
    qc: str = Field(..., description="Quantum circuit string in QASM format")


class TaskResponse(BaseModel):
    """
    Data model representing a task submission response
    """
    task_id: str
    message: str


class TaskStatusResponse(BaseModel):
    """
    Data model representing a task status response
    """
    status: str
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
