import httpx
import asyncio

"""
This test demonstrates true async behavior using FastAPI + Celery + Redis.
It sends multiple tasks and polls their results concurrently.
"""

API_URL = "http://127.0.0.1:8000"

qc_samples = [
    "OPENQASM 3; include \"stdgates.inc\"; qubit[2] q; bit[2] c; h q[0]; cx q[0], q[1]; c = measure q;",
    "OPENQASM 3; include \"stdgates.inc\"; qubit[2] q; bit[2] c; h q[0]; cx q[0], q[1]; c = measure q;",
    "OPENQASM 3; include \"stdgates.inc\"; qubit[2] q; bit[2] c; h q[0]; cx q[0], q[1]; c = measure q;",
    "OPENQASM 3; include \"stdgates.inc\"; qubit[2] q; bit[2] c; h q[0]; cx q[0], q[1]; c = measure q;",
    "OPENQASM 3; include \"stdgates.inc\"; qubit[2] q; bit[2] c; h q[0]; cx q[0], q[1]; c = measure q;"
]


async def post_task(client, qc_str):
    response = await client.post(f"{API_URL}/tasks", json={"qc": qc_str})
    data = response.json()
    return data["task_id"]


async def get_task(client, task_id):
    while True:
        response = await client.get(f"{API_URL}/tasks/{task_id}")
        data = response.json()
        if data["status"] == "completed":
            print(f"[✅] Task {task_id} completed:", data["result"])
            return
        elif data["status"] == "error":
            print(f"[❌] Task {task_id} failed:", data["message"])
            return
        else:
            print(f"[⏳] Task {task_id} is still running...")
            await asyncio.sleep(1.5)


async def main():
    async with httpx.AsyncClient(timeout=30) as client:
        # Submit all tasks concurrently
        post_tasks = [post_task(client, qc) for qc in qc_samples]
        task_ids = await asyncio.gather(*post_tasks)

        print("Submitted all tasks, now polling for results...\n")

        # Poll all tasks concurrently
        get_tasks = [get_task(client, task_id) for task_id in task_ids]
        await asyncio.gather(*get_tasks)

if __name__ == "__main__":
    asyncio.run(main())
