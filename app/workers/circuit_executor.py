import time

# Pure function definitions with no direct Celery dependencies
# This separates the business logic from the task machinery


def execute_quantum_circuit(qc_string):
    """
    Execute a quantum circuit from its QASM string representation

    This contains the core business logic for quantum circuit execution
    without any dependency on Celery.
    """
    # In a real implementation, this would parse the QASM and execute on a simulator or real quantum device
    time.sleep(2)  # Simulating processing time
    return {"message": "Circuit executed successfully", "input": qc_string}


def execute_dummy_circuit(qc_string):
    """
    A dummy implementation for testing purposes
    """
    time.sleep(2)
    return {"message": "Executed dummy task", "input": qc_string}
