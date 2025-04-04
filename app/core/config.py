import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger("api")

# Redis and Celery configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "0")

# Construct URLs
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
BROKER_URL = os.getenv("BROKER_URL", REDIS_URL)
RESULT_BACKEND = os.getenv("RESULT_BACKEND", REDIS_URL)

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

logger.info(f"Configuration loaded. Environment: {ENVIRONMENT}")
logger.info(f"Redis URL: {REDIS_URL}")

# Application settings
APP_NAME = "Quantum Circuits System"
APP_VERSION = "1.0.0"
