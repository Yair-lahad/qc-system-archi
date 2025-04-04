"""
tasks.py - Celery worker logic for executing QASM3 quantum circuits.

Responsible for:
- Parsing QASM3 input
- Executing with Qiskit AerSimulator
- Formatting result counts
"""
import logging
from app.core.celery_app import celery_app
from qiskit import qasm3, QuantumCircuit
from qiskit_aer import AerSimulator

logger = logging.getLogger("worker")


def execute_quantum_circuit(qasm_str: str) -> dict:
    """
    Parses and executes a QASM3 circuit using Qiskit AerSimulator.
    Args:
        qc_string (str): A valid quantum circuit in QASM3 format.
    Returns:
        dict: Counts result (measurement outcomes) or error payload.
    """
    try:
        # Deserialize QASM3 to QuantumCircuit
        qc: QuantumCircuit = qasm3.loads(qasm_str)
        # Run the circuit on AerSimulator
        simulator = AerSimulator()
        result = simulator.run(qc, shots=1024).result()
        counts = result.get_counts()
        logger.info(f"Execution result: {counts}")
        return counts

    except Exception as e:
        logger.exception("Failed to parse or execute QASM3 circuit")
        error_msg = str(e) or e.__class__.__name__
        return {"error": f"QASM3 execution failed: {error_msg}"}


@celery_app.task(name="app.workers.tasks.execute_circuit_task")
def execute_circuit_task(qasm_str: str) -> dict:
    """
    Celery task to run a QASM3 quantum circuit.
    """
    return execute_quantum_circuit(qasm_str)
