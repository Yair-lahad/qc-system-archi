from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
import celery.exceptions
import logging
from app.core.celery_app import celery_app
from app.core.redis_client import get_redis_client

logger = logging.getLogger("api")
router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """Overall system health check"""
    logger.debug("Performing complete health check")

    redis_health = check_redis_health()
    celery_health = check_celery_health()

    # Determine overall status
    overall_status = "ok"
    if redis_health != "healthy" or celery_health != "healthy":
        overall_status = "degraded"

    return {
        "status": overall_status,
        "components": {
            "api": "healthy",
            "celery": celery_health,
            "redis": redis_health
        }
    }


@router.get("/ping")
async def ping():
    """Simple ping endpoint for basic liveness probe"""
    return {"status": "ok"}


@router.get("/redis")
async def redis_health(redis: Redis = Depends(get_redis_client)):
    """Check Redis connection"""
    logger.debug("Checking Redis health")
    try:
        redis.ping()
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        raise HTTPException(
            status_code=503, detail=f"Redis unhealthy: {str(e)}")


@router.get("/celery")
async def celery_health():
    """Check Celery workers status"""
    logger.debug("Checking Celery health")
    status = check_celery_health()
    if status == "healthy":
        return {"status": "healthy"}
    else:
        raise HTTPException(
            status_code=503, detail=f"Celery unhealthy: {status}")


def check_redis_health():
    """Check Redis connection and return status string"""
    try:
        redis = get_redis_client()
        redis.ping()
        return "healthy"
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        return f"unhealthy: {str(e)}"


def check_celery_health():
    """Check Celery workers and return status string"""
    try:
        inspector = celery_app.control.inspect()
        workers = inspector.ping()

        if not workers:
            return "no workers available"

        # Check if all workers responded successfully
        for worker, response in workers.items():
            if not response.get('ok'):
                return f"worker {worker} not responding properly"

        return "healthy"
    except celery.exceptions.CeleryError as e:
        logger.error(f"Celery health check failed: {str(e)}")
        return f"error: {str(e)}"
    except Exception as e:
        logger.exception(f"Unexpected error in Celery health check: {str(e)}")
        return f"error: {str(e)}"
