import redis
import logging
from functools import lru_cache
from app.core.config import REDIS_URL

logger = logging.getLogger("redis")


@lru_cache()
def get_redis_client():
    """
    Returns a Redis client instance
    Uses connection pooling and caches the client
    """
    logger.info(f"Initializing Redis client with URL: {REDIS_URL}")

    try:
        # Create a connection pool
        pool = redis.ConnectionPool.from_url(
            url=REDIS_URL,
            max_connections=10,
            socket_timeout=5.0,
            socket_connect_timeout=5.0
        )

        # Create client from pool
        client = redis.Redis(connection_pool=pool)

        # Test connection
        client.ping()
        logger.info("Redis connection successful")

        return client
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Redis connection error: {str(e)}")
        # Return client anyway, let the application handle connection issues
        return redis.Redis.from_url(REDIS_URL)
    except Exception as e:
        logger.exception(f"Unexpected Redis error: {str(e)}")
        raise
