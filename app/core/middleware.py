import time
import logging
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger("api")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Middleware that logs incoming requests and outgoing responses
        with timing information and request details
        """
        start_time = time.time()
        request_id = str(request.headers.get("X-Request-Id", ""))

        # Create log context with basic request info
        log_context = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else None,
        }

        # Log the start of request processing
        logger.info(f"Request started: {json.dumps(log_context)}")

        # Process the request and catch any exceptions
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            # Log any unhandled exceptions
            logger.exception(f"Unhandled exception: {str(e)}")
            # Re-raise to let FastAPI handle the error response
            raise
        finally:
            # Calculate processing time
            process_time = time.time() - start_time

        # Add response info to context
        log_context.update({
            "status_code": status_code,
            "processing_time_ms": round(process_time * 1000, 2)
        })

        # Log completion with appropriate level based on status code
        if status_code >= 500:
            logger.error(f"Request failed: {json.dumps(log_context)}")
        elif status_code >= 400:
            logger.warning(f"Request error: {json.dumps(log_context)}")
        else:
            logger.info(f"Request completed: {json.dumps(log_context)}")

        return response
