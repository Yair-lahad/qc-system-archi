from app.core.celery_app import celery_app
from app.workers.circuit_executor import execute_quantum_circuit, execute_dummy_circuit

# This module is responsible for registering task functions with Celery
# It keeps the Celery-specific code separate from the business logic

# Register the execute_quantum_circuit function as a Celery task
execute_circuit_task = celery_app.task(
    name="app.workers.circuit_executor.execute_quantum_circuit"
)(execute_quantum_circuit)
# Register the execute_dummy_circuit function as a Celery task
dummy_task = celery_app.task(
    name="app.workers.circuit_executor.execute_dummy_circuit"
)(execute_dummy_circuit)
