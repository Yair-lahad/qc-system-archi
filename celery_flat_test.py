from celery import Celery

app = Celery('simple',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

@app.task
def add(x, y):
    print("INSIDE ADD")
    return x + y
