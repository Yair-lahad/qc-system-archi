# Quantum Circuits System Architecture program

This project sets up a minimal async task processing system using FastAPI, Celery, and Redis.

## How to Run

1. Build and run:
```bash
docker-compose up --build
```

2. Access the API:
- POST /tasks → Submit dummy task
- GET /tasks/<task_id> → Poll result

3. Run tests (while system is running):
```bash
pytest tests/
```

Start coding from here!