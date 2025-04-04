import pytest
import httpx
import asyncio

API_URL = "http://api:8000"  # 'api' is the service name in docker-compose


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
                assert any(k in data["result"] for k in ["00", "11", "01", "10"])
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
            get = await client.get(f"/tasks/{task_id}")
            data = get.json()
            if data["status"] == "completed":
                assert "error" in data["result"]
                return
            await asyncio.sleep(1)
        assert False, "Task did not complete with error as expected"


@pytest.mark.asyncio
async def test_dispatcher_validation_rejects_bad_input():
    async with httpx.AsyncClient(base_url=API_URL) as client:
        post = await client.post("/tasks", json={})
        assert post.status_code == 422
        assert "detail" in post.json()
