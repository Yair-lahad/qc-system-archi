import logging
from app.core.celery_app import celery_app
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

logger = logging.getLogger("worker")


def execute_quantum_circuit(qc_string: str) -> dict:
    """
    Simulates execution of a quantum circuit.

    Currently uses a fixed Bell state circuit as a placeholder
    while QASM3 deserialization is deferred.
    """
    logger.info("Starting quantum circuit execution")

    try:
        # TODO: Replace this hardcoded Bell circuit with qasm3.loads(qc_string)
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()
        simulator = AerSimulator()
        result = simulator.run(qc, shots=1024).result()
        counts = result.get_counts()
        logger.info(f"Raw counts: {counts}")
        # Format to match the required output schema:
        # counts measured in basis states like '00', '11' etc.
        formatted_counts = {"0": 0, "1": 0}
        for outcome, count in counts.items():
            if outcome.startswith("00"):
                formatted_counts["0"] += count
            elif outcome.startswith("11"):
                formatted_counts["1"] += count
        logger.info(f"Formatted counts: {formatted_counts}")
        return formatted_counts
    except Exception as e:
        logger.exception("Quantum circuit execution failed")
        return {"error": f"Circuit execution failed: {str(e)}"}


@celery_app.task(name="app.workers.tasks.execute_circuit_task")
def execute_circuit_task(qasm_str: str) -> dict:
    """
    Celery task wrapper to execute a quantum circuit from a QASM3 string (placeholder for now).
    """
    return execute_quantum_circuit(qasm_str)
