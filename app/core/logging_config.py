import os
import logging.config
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Get log level from environment or use INFO as default
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logging():
    """Configure logging for the application"""
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": LOG_LEVEL,
            },
            "api_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "logs/api.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "level": LOG_LEVEL,
            },
            "worker_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "logs/worker.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "level": LOG_LEVEL,
            },
            "redis_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "logs/redis.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "level": LOG_LEVEL,
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console"],
                "level": LOG_LEVEL,
            },
            "api": {
                "handlers": ["console", "api_file"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "worker": {
                "handlers": ["console", "worker_file"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "redis": {
                "handlers": ["console", "redis_file"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console", "api_file"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "celery": {
                "handlers": ["console", "worker_file"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
        },
    }

    # Apply configuration
    logging.config.dictConfig(logging_config)

    # Log startup message
    logging.getLogger("api").info("Logging configured successfully")
