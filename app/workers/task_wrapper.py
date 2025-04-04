import time
import logging
import functools
from app.core.redis_client import get_redis_client

logger = logging.getLogger("worker")


def task_with_metrics(task_func):
    """
    Decorator for Celery tasks to add timing metrics and error tracking
    """
    @functools.wraps(task_func)
    def wrapper(self, *args, **kwargs):
        task_id = self.request.id
        task_name = task_func.__name__

        # Log task start
        logger.info(f"Task {task_name}[{task_id}] started")

        # Update metrics - increment total tasks
        try:
            redis = get_redis_client()
            redis.incr('stats:total_tasks')
        except Exception as e:
            logger.warning(f"Could not update task metrics: {str(e)}")

        # Execute task with timing
        start_time = time.time()
        try:
            result = task_func(self, *args, **kwargs)
            execution_time = time.time() - start_time

            # Log task completion
            logger.info(
                f"Task {task_name}[{task_id}] completed successfully in {execution_time:.4f}s")

            # Update metrics
            try:
                redis = get_redis_client()

                # Increment completed tasks counter
                redis.incr('stats:completed_tasks')

                # Update average execution time (simple moving average)
                current_avg = float(redis.get('stats:avg_execution_time') or 0)
                count = int(redis.get('stats:completed_tasks') or 1)
                # Simple moving average calculation
                new_avg = current_avg + (execution_time - current_avg) / count
                redis.set('stats:avg_execution_time', new_avg)

                # Store task metadata
                redis.hset(
                    f'task:{task_id}',
                    mapping={
                        'name': task_name,
                        'status': 'completed',
                        'execution_time': execution_time,
                        'completed_at': time.time()
                    }
                )
                # Expire task metadata after 1 hour
                redis.expire(f'task:{task_id}', 3600)

            except Exception as e:
                logger.warning(
                    f"Could not update task completion metrics: {str(e)}")

            return result

        except Exception as e:
            execution_time = time.time() - start_time

            # Log task failure
            logger.error(
                f"Task {task_name}[{task_id}] failed after {execution_time:.4f}s: {str(e)}",
                exc_info=True
            )

            # Update metrics
            try:
                redis = get_redis_client()
                redis.incr('stats:failed_tasks')

                # Store task metadata
                redis.hset(
                    f'task:{task_id}',
                    mapping={
                        'name': task_name,
                        'status': 'failed',
                        'error': str(e),
                        'execution_time': execution_time,
                        'failed_at': time.time()
                    }
                )
                # Expire task metadata after 1 day (keep failures longer for debugging)
                redis.expire(f'task:{task_id}', 86400)

            except Exception as err:
                logger.warning(
                    f"Could not update task failure metrics: {str(err)}")

            # Re-raise the original exception
            raise

    return wrapper
