from fastapi import APIRouter, Depends
import logging
from app.core.redis_client import get_redis_client

logger = logging.getLogger("api")
router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/")
async def get_metrics(redis=Depends(get_redis_client)):
    """Get basic system metrics"""
    logger.debug("Retrieving system metrics")

    try:
        # Basic Redis stats
        info = redis.info()

        # Celery task metrics from Redis
        pending_tasks = 0
        active_tasks = 0
        reserved_tasks = 0

        # Try to get Celery task metrics using pattern search
        task_keys = redis.keys('celery-task-meta-*')
        completed_tasks = len(task_keys)

        # Get custom metrics if available
        total_tasks = int(redis.get('stats:total_tasks') or 0)
        failed_tasks = int(redis.get('stats:failed_tasks') or 0)

        # If we don't have total tasks stats, use completed + pending as estimate
        if total_tasks == 0:
            total_tasks = max(completed_tasks, 1)  # Avoid division by zero

        # Calculate success rate
        success_rate = (completed_tasks - failed_tasks) / \
            total_tasks * 100 if total_tasks > 0 else 0

        return {
            "queue_stats": {
                "pending_tasks": pending_tasks,
                "active_tasks": active_tasks,
                "reserved_tasks": reserved_tasks,
                "completed_tasks": completed_tasks,
            },
            "task_stats": {
                "total": total_tasks,
                "completed": completed_tasks,
                "failed": failed_tasks,
                "success_rate": round(success_rate, 2)
            },
            "redis_stats": {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "N/A"),
                "total_commands_processed": info.get("total_commands_processed", 0)
            }
        }
    except Exception as e:
        logger.exception(f"Error retrieving metrics: {str(e)}")
        return {
            "status": "error",
            "message": f"Error retrieving metrics: {str(e)}"
        }


@router.get("/tasks")
async def get_task_metrics(redis=Depends(get_redis_client)):
    """Get detailed task processing metrics"""
    logger.debug("Retrieving task metrics")

    try:
        # Get stored task timing metrics if available
        avg_execution_time = float(redis.get('stats:avg_execution_time') or 0)

        return {
            "timing": {
                "avg_execution_time_ms": round(avg_execution_time * 1000, 2)
            }
        }
    except Exception as e:
        logger.exception(f"Error retrieving task metrics: {str(e)}")
        return {
            "status": "error",
            "message": f"Error retrieving task metrics: {str(e)}"
        }
