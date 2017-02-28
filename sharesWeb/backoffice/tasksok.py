import globalVars
from celery import Celery

try:
    app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')
except Exception as e:
    globalVars.toLogFile('Error inicializando taskscelery: ' + str(e))


@app.task
def add(x, y):
    return x + y

