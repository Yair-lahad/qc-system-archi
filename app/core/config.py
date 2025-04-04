import logging
from dotenv import load_dotenv
import os

# Always load .env.docker first if it exists
if os.path.exists(".env.docker"):
    load_dotenv(dotenv_path=".env.docker")
else:
    load_dotenv()

print("ENVIRONMENT =", os.getenv("ENVIRONMENT"))
print("REDIS_HOST =", os.getenv("REDIS_HOST"))
logger = logging.getLogger("api")

# Redis and Celery configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "0")

# Construct Redis URL
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
BROKER_URL = os.getenv("BROKER_URL", REDIS_URL)
RESULT_BACKEND = os.getenv("RESULT_BACKEND", REDIS_URL)

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

logger.info(f"Configuration loaded. Environment: {ENVIRONMENT}")
logger.info(f"Redis URL: {REDIS_URL}")
if REDIS_HOST == "localhost" and ENVIRONMENT == "production":
    logger.warning(
        "⚠️ Docker environment is using localhost Redis. This may cause connection errors. Check .env.docker or ENV settings.")


# Application settings
APP_NAME = "Quantum Circuits System"
APP_VERSION = "1.0.0"
