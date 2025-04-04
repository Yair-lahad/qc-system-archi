import logging
from fastapi import FastAPI
from app.api import routes
from app.api import health
from app.api import metrics
from app.core.middleware import LoggingMiddleware
from app.core.logging_config import setup_logging

# Setup logging first
setup_logging()
logger = logging.getLogger("api")

# Initialize FastAPI app
app = FastAPI(
    title="Quantum Circuits System",
    description="API for executing and monitoring quantum circuits",
    version="1.0.0"
)

# Add middleware for request/response logging
app.add_middleware(LoggingMiddleware)

# Include API routers
app.include_router(routes.router)
app.include_router(health.router)
app.include_router(metrics.router)


@app.on_event("startup")
async def startup_event():
    """Runs when the application starts"""
    logger.info("Starting Quantum Circuits API server")


@app.on_event("shutdown")
async def shutdown_event():
    """Runs when the application shuts down"""
    logger.info("Shutting down Quantum Circuits API server")

# Root endpoint for basic info


@app.get("/")
async def root():
    """Root endpoint providing basic API information"""
    return {
        "name": "Quantum Circuits API",
        "version": "1.0.0",
        "status": "running"
    }
