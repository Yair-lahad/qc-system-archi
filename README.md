# Quantum Circuit Execution System 

A containerized system for asynchronous quantum circuit execution using FastAPI, Celery, and Redis.

This system is a 48 hours Job Interview Project focuses on robust task processing with high availability and integrity.

## System Architecture

The Structure follows a modular, layered architecture with clear boundaries between components, enabling containerization and maintainability.

### Key Components

#### 1. API Layer (FastAPI)
- API endpoints for submitting and retrieving quantum circuits
- Asynchronous request handling
- Decoupled from processing logic for independent deployment and scaling

#### 2. Interface Layer (Task Dispatcher)
- Clear boundary between API and workers enables separation
- Centralizes complex task logic for better maintainability
- Abstraction layer allows swapping implementation details without API changes

#### 3. Message Queue (Redis + Celery)
- Ensures task integrity and persistence
- Reliable fully asynchronous task processing
- Decouple producers from consumers for independent scaling

#### 4. Worker Layer
- Isolated execution of Quantum Circuit logic prevents cascading failures
- Support robust and containerized deployment
- Independent scaling based on processing demands

## Project Structure

```
quantum-circuit-system/
├── app/
│   ├── api/                    ## API endpoints and request handling
│   │   ├── health.py             # Health check endpoints
│   │   ├── metrics.py            # Metrics endpoints
│   │   └── routes.py             # Main API routes
│   ├── core/                   ## Core application components
│   │   ├── celery_app.py         # Celery configuration
│   │   ├── config.py             # Application configuration
│   │   ├── logging_config.py     # Logging setup
│   │   ├── middleware.py         # Request/response middleware
│   │   ├── models.py             # Data models
│   │   └── redis_client.py       # Redis connection
│   ├── interface/              ## Interface between API and workers
│   │   └── dispatcher.py         # Task dispatching
│   ├── workers/                ## Worker processes
│   │   ├── task_wrapper.py       # Task metrics and monitoring
│   │   └── tasks.py              # Task definitions
│   └── main.py                 ## Application entry point
├── tests/                      ## Test suite
│   └── test_api.py               # API integration tests
├── docker-compose.yaml           # Container orchestration
├── Dockerfile.api                # API container
├── Dockerfile.worker             # Worker container
├── .env.docker                   # Docker environment variables
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## How to Run

### Getting Started

### Quick Start

0. Prerequisites:

   Docker + Docker Compose installed (Docker Desktop recommended)

1. Clone the repository:
```bash
git clone https://github.com/Yair-lahad/qc-system-archi.git
cd qc-system-archi
```

   - If you're starting from scratch, you can create a new repository and copy these files into it.
   - Alternatively, you can fork this repository to your GitHub account.

2. Start the system using Docker Compose:
```bash
docker-compose up --build
```

3. Access the API documentation:
```
http://localhost:8000/docs
```

### Running Tests

Run the test suite with:
```bash
docker-compose up -d  # in order for the app to be live behind the scenes
docker-compose run --rm test
```

## API Endpoints

### Submit Quantum Circuit
```
POST /tasks
```

Request:
```json
{
  "qc": "OPENQASM 3; include \"stdgates.inc\"; qubit[2] q; bit[2] c; h q[0]; cx q[0], q[1]; c = measure q;"
}
```

Response:
```json
{
  "task_id": "8f1c3d9e-4a5b-6c7d-8e9f-0a1b2c3d4e5f",
  "message": "Task submitted successfully."
}
```

### Get Task Status/Result
```
GET /tasks/{task_id}
```

Response (pending):
```json
{
  "status": "pending",
  "message": "Task is still in progress."
}
```

Response (completed):
```json
{
  "status": "completed",
  "result": {
    "00": 512,
    "11": 512
  }
}
```

### Health Checks
```
GET /health
```

Response:
```json
{
  "status": "ok",
  "components": {
    "api": "healthy",
    "celery": "healthy",
    "redis": "healthy"
  }
}
```

### Metrics
```
GET /metrics
```

Response:
```json
{
  "queue_stats": {
    "pending_tasks": 0,
    "active_tasks": 0,
    "reserved_tasks": 0,
    "completed_tasks": 124
  },
  "task_stats": {
    "total": 125,
    "completed": 124,
    "failed": 1,
    "success_rate": 99.2
  },
  "redis_stats": {
    "connected_clients": 4,
    "used_memory_human": "1.2M",
    "total_commands_processed": 8564
  }
}
```

## Key Features

### 1. Asynchronous Processing & Task Integrity
- Tasks are processed asynchronously via Celery
- Redis ensures task persistence and prevents task loss
- Task state is tracked and retrievable at any time

### 2. Containerization & Orchestration
- Docker containers for all system components
- Docker Compose for service orchestration
- Volume mounts for logs and Redis data persistence

### 3. Robustness & Error Handling
- Comprehensive error handling for all operations
- Detailed logging for debugging and monitoring
- Health checks for system component monitoring
- Graceful degradation when components fail

### 4. Scalability
- Horizontally scalable worker processes
- Connection pooling for Redis
- Efficient resource utilization

## Development

### Local Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start Redis locally:
```bash
docker run -p 6379:6379 redis:latest
```

4. Run the API server:
```bash
uvicorn app.main:app --reload
```

5. Start a Celery worker:
```bash
celery -A app.core.celery_app worker --loglevel=info --pool=solo
```

## Examples

### Example: Bell State Circuit

```python
import requests

# Bell state circuit in QASM3 format
bell_circuit = """
OPENQASM 3;
include "stdgates.inc";
qubit[2] q;
bit[2] c;
h q[0];
cx q[0], q[1];
c = measure q;
"""

# Submit the circuit
response = requests.post(
    "http://localhost:8000/tasks",
    json={"qc": bell_circuit}
)
task_id = response.json()["task_id"]
print(f"Task submitted with ID: {task_id}")

# Poll for results
while True:
    result = requests.get(f"http://localhost:8000/tasks/{task_id}")
    data = result.json()
    if data["status"] == "completed":
        print("Circuit execution results:")
        print(data["result"])
        break
    elif data["status"] == "error":
        print(f"Error: {data['message']}")
        break
    print("Still processing...")
    import time
    time.sleep(1)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.