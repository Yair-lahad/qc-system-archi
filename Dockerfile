# Dockerfile.api
# FROM python:3.9-slim
# WORKDIR /app
# COPY . .
# RUN pip install --no-cache-dir -r requirements.txt
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# # Dockerfile.worker
# FROM python:3.9-slim
# WORKDIR /app
# COPY . .
# RUN pip install --no-cache-dir -r requirements.txt
# CMD ["celery", "-A", "app.core.celery_app", "worker", "--loglevel=info"]