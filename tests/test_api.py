import pytest
import httpx
import asyncio

API_URL = "http://api:8000"  # 'api' is the service name in docker-compose
QASM = 'OPENQASM 3; include "stdgates.inc"; qubit[1] q; bit[1] c; h q[0]; c = measure q;'


@pytest.mark.asyncio
async def test_valid_qasm_submission_and_result():
    qasm = 'OPENQASM 3; include "stdgates.inc"; qubit[2] q; bit[2] c; h q[0]; cx q[0], q[1]; c = measure q;'
    async with httpx.AsyncClient(base_url=API_URL) as client:
        # Submit task
        post = await client.post("/tasks", json={"qc": qasm})
        assert post.status_code == 200
        task_id = post.json()["task_id"]

        # Poll for result
        for _ in range(15):
            get = await client.get(f"/tasks/{task_id}")
            data = get.json()
            if data["status"] == "completed":
                # Updated assertion: expect result keys to be "0" and/or "1"
                assert set(data["result"].keys()).issubset({"0", "1"})
                return
            await asyncio.sleep(1)
        assert False, "Task did not complete in time"


@pytest.mark.asyncio
async def test_invalid_qasm_returns_error():
    bad_qasm = "OPENQASM 3; bad syntax;"
    async with httpx.AsyncClient(base_url=API_URL) as client:
        post = await client.post("/tasks", json={"qc": bad_qasm})
        assert post.status_code == 200
        task_id = post.json()["task_id"]

        for _ in range(10):
            res = await client.get(f"/tasks/{task_id}")
            data = res.json()
            # Handle edge cases like missing task or immediate error
            if "status" in data:
                if data["status"] == "error":
                    assert "message" in data
                    return
                elif data["status"] == "completed":
                    assert "error" in data["result"]
                    return
            await asyncio.sleep(0.5)
        assert False, "Task did not return error as expected"


@pytest.mark.asyncio
async def test_dispatcher_validation_rejects_bad_input():
    async with httpx.AsyncClient(base_url=API_URL) as client:
        post = await client.post("/tasks", json={})
        assert post.status_code == 422
        assert "detail" in post.json()


@pytest.mark.asyncio
async def test_concurrent_task_execution():
    async def submit_and_poll(client):
        post = await client.post("/tasks", json={"qc": QASM})
        assert post.status_code == 200
        task_id = post.json()["task_id"]

        # Poll for result
        for _ in range(20):
            res = await client.get(f"/tasks/{task_id}")
            data = res.json()
            if data["status"] == "completed":
                assert set(data["result"].keys()).issubset({"0", "1"})
                return
            await asyncio.sleep(0.2)

        assert False, f"Task {task_id} did not complete in time"

    async with httpx.AsyncClient(base_url=API_URL) as client:
        task_count = 10  # Adjust to stress system (e.g., 50)
        await asyncio.gather(*(submit_and_poll(client) for _ in range(task_count)))
