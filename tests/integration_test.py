import time
import requests

BASE_URL = "http://localhost:8000"

def test_dummy_task_flow():
    response = requests.post(f"{BASE_URL}/tasks", json={"qc": "demo_circuit"})
    assert response.status_code == 200
    task_id = response.json()["task_id"]

    for _ in range(10):
        res = requests.get(f"{BASE_URL}/tasks/{task_id}")
        status = res.json().get("status")
        if status == "completed":
            assert "result" in res.json()
            break
        time.sleep(1)
    else:
        assert False, "Task did not complete in time"