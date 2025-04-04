# Quantum Circuits System Architecture

This project implements a robust, asynchronous system for executing quantum circuits using FastAPI, Celery, and Redis.

## Architecture Overview

### System Components

#### 1. API Layer (FastAPI)
The API layer handles HTTP requests and responses, providing endpoints for submitting quantum circuits and retrieving results. It's built with FastAPI for high performance and ease of development.

#### 2. Interface Layer (Dispatcher)
The dispatcher serves as a critical interface between the API and worker layers. It has several important responsibilities:

- **Separation of Concerns**: Isolates API code from task processing details
- **Task Management**: Provides a centralized interface for submitting tasks and retrieving results
- **Abstraction**: Shields the API from the specifics of the task queue implementation
- **Consistency**: Ensures uniform handling of task submission and retrieval throughout the application
- **Maintainability**: Makes it easier to change task processing behavior without affecting API code

Without the dispatcher, the API endpoints would need to interact directly with Celery, coupling the API code to the specific task queue implementation. The dispatcher provides a clean boundary that improves code organization and maintainability.

#### 3. Task Queue (Celery + Redis)
The task queue system manages asynchronous processing of quantum circuit tasks:

- **Celery**: Handles task definition, dispatching, and execution
- **Redis**: Acts as the message broker and result backend
- **Task Registration**: Defines what tasks are available for execution
- **Task Execution**: Processes the quantum circuits asynchronously

#### 4. Worker Layer
The worker layer contains the business logic for executing quantum circuits:

- **Task Functions**: Pure functions that execute quantum circuits without Celery dependencies
- **Celery Tasks**: Wrapper functions that integrate with Celery for asynchronous processing
- **Task Monitoring**: Logs and metrics collection for observability

### Communication Flow

1. A client submits a quantum circuit to the API (`POST /tasks`)
2. The API route passes the circuit to the dispatcher
3. The dispatcher submits the task to Celery and returns a task ID
4. The API returns the task ID to the client
5. Celery routes the task to an available worker
6. The worker executes the quantum circuit
7. Results are stored in Redis
8. When the client requests results (`GET /tasks/{id}`), the API uses the dispatcher to retrieve them from Redis

### Observability Features

The system includes comprehensive observability features:

- **Health Checks**: Endpoints to verify the health of each component
- **Logging**: Detailed logs for API requests, task execution, and system events
- **Metrics**: Collection of performance and utilization metrics

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9 or higher (for local development)
- Redis (for local development without Docker)

### Running with Docker Compose

1. Clone the repository:
   ```
   git clone <repository-url>
   cd quantum-circuits-system
   ```

2. Build and start the containers:
   ```
   docker-compose up --build
   ```

3. Access the API:
   - API documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

### Running Locally for Development

1. Start Redis (using Docker):
   ```
   docker run --name my-redis -p 6379:6379 -d redis:latest
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   LOG_LEVEL=INFO
   ENVIRONMENT=development
   ```

4. Start the FastAPI server (in one terminal):
   ```
   uvicorn app.main:app --reload
   ```

5. Start a Celery worker (in another terminal):
   ```
   celery -A app.core.celery_app worker --loglevel=info
   ```

## API Endpoints

### Submit a Quantum Circuit
```
POST /tasks
```

Request body:
```json
{
  "qc": "<serialized_quantum_circuit_in_qasm3>"
}
```

Response:
```json
{
  "task_id": "12345",
  "message": "Task submitted successfully."
}
```

### Get Task Result
```
GET /tasks/{task_id}
```

Response (completed):
```json
{
  "status": "completed",
  "result": {"message": "Circuit executed successfully", "input": "..."}
}
```

Response (pending):
```json
{
  "status": "pending",
  "message": "Task is still in progress."
}
```

### Health Check
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

## Running Tests

With the system running (either via Docker Compose or locally):

```
pytest tests/
```

## Project Structure

```
quantum-circuits-system/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── health.py         # Health check endpoints
│   │   ├── metrics.py        # Metrics endpoints
│   │   └── routes.py         # API route definitions
│   ├── core/
│   │   ├── __init__.py
│   │   ├── celery_app.py     # Celery configuration
│   │   ├── config.py         # Application configuration
│   │   ├── logging_config.py # Logging setup
│   │   ├── middleware.py     # FastAPI middleware
│   │   ├── models.py         # Data models
│   │   └── redis_client.py   # Redis connection
│   ├── interface/
│   │   ├── __init__.py
│   │   └── dispatcher.py     # Task dispatcher
│   ├── workers/
│   │   ├── __init__.py
│   │   └── tasks.py          # Task definitions
│   ├── __init__.py
│   └── main.py               # Application entry point
├── tests/
│   ├── __init__.py
│   ├── integration_test.py   # Integration tests
│   └── simple_api_test.py    # Basic API tests
├── .env                      # Local environment variables
├── .env.docker              # Docker environment variables
├── .gitignore               # Git ignore file
├── Dockerfile.api           # API container definition
├── Dockerfile.worker        # Worker container definition
├── LICENSE                  # Project license
├── README.md                # This file
├── docker-compose.yaml      # Container orchestration
└── requirements.txt         # Python dependencies
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.