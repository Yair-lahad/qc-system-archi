from app.workers.tasks import add

if __name__ == '__main__':
    result = add.delay(2, 3)
    print("Task sent. Waiting for result...")
    print(f"Task result: {result.get(timeout=10)}")