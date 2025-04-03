# Quantum Circuits System Architecture program

This project sets up a minimal async task processing system using FastAPI, Celery, and Redis.

## How to Run

1. Build and run:
```bash
docker-compose up --build
 ** make sure you have docker-compose installed at your machine.
```

2. Access the API:
- POST /tasks → Submit dummy task
- GET /tasks/<task_id> → Poll result

3. Run tests (while system is running):
```bash
pytest tests/
```

Start coding from here!

## More on Architecture of the System

Structure is Containerized by docker-compose using 2 different Dockerfile.
Dockerfile.api is responsible for the Server API by FastAPI module which routes our POST and GET calls and interacts with a Client.
Dockerfile.worker is responsible for the actual behind the scene work of the qc by Celery module.
both Dockerfile share an instance of Celery_app and depends on Redis server, maintaining consistency and effective asyncronous processing throuout the program.