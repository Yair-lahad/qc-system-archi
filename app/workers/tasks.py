from app.core.celery_app import celery_app
import time


@celery_app.task(name="execute_quantum_circuit")
def execute_quantum_circuit(qc_string):
    """
    Execute a quantum circuit from its QASM string representation
    """
    # In a real implementation, this would parse the QASM and execute on a simulator or real quantum device
    time.sleep(2)  # Simulating processing time
    return {"message": "Circuit executed successfully", "input": qc_string}


@celery_app.task(name="execute_dummy_circuit")
def execute_dummy_circuit(qc_string):
    """
    A dummy implementation for testing purposes
    """
    time.sleep(2)
    return {"message": "Executed dummy task", "input": qc_string}
