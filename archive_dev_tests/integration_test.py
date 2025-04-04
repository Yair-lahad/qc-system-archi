import time
import requests
import pytest

BASE_URL = "http://localhost:8000"


def test_quantum_circuit_flow():
    """Test the end-to-end flow of submitting and retrieving a quantum circuit task."""

    # Example QASM3 - simple Bell state circuit
    test_qasm = """
    OPENQASM 3;
    include "stdgates.inc";
    qubit[2] q;
    bit[2] c;
    h q[0];
    cx q[0], q[1];
    c = measure q;
    """

    # Submit the task
    response = requests.post(f"{BASE_URL}/tasks", json={"qc": test_qasm})
    assert response.status_code == 200
    response_data = response.json()
    assert "task_id" in response_data
    assert "message" in response_data
    assert response_data["message"] == "Task submitted successfully."

    task_id = response_data["task_id"]

    # Poll for the result (with timeout)
    for _ in range(30):  # Try for 30 seconds
        res = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert res.status_code == 200

        result_data = res.json()
        status = result_data.get("status")

        if status == "error":
            pytest.fail(
                f"Task failed with error: {result_data.get('message')}")

        if status == "completed":
            # Verify the structure of the result
            assert "result" in result_data
            counts = result_data["result"]

            # For a Bell state, we expect only |00⟩ and |11⟩ states with roughly equal probabilities
            assert isinstance(counts, dict)
            assert len(counts) > 0

            # All keys should be bit strings
            for key in counts.keys():
                assert all(bit in '01' for bit in key)

            return  # Test passed

        time.sleep(1)

    pytest.fail("Task did not complete within the timeout period")


def test_error_handling():
    """Test the API's error handling for invalid inputs and non-existent tasks."""

    # Test invalid input
    response = requests.post(f"{BASE_URL}/tasks", json={"qc": ""})
    assert response.status_code != 200  # Should reject empty circuit

    # Test non-existent task
    response = requests.get(f"{BASE_URL}/tasks/nonexistent-task-id")
    assert response.status_code == 404
    
# import time
# import requests

# BASE_URL = "http://localhost:8000"

# def test_dummy_task_flow():
#     response = requests.post(f"{BASE_URL}/tasks", json={"qc": "demo_circuit"})
#     assert response.status_code == 200
#     task_id = response.json()["task_id"]

#     for _ in range(10):
#         res = requests.get(f"{BASE_URL}/tasks/{task_id}")
#         status = res.json().get("status")
#         if status == "completed":
#             assert "result" in res.json()
#             break
#         time.sleep(1)
#     else:
#         assert False, "Task did not complete in time"
