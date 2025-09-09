import os
from time import sleep

from celery import Celery, Task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'svango.config.settings')

app = Celery('svango')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=False)
def debug_task(task:Task, x:int, y:int, wait:int=1) -> int:
    task.request.meta = {'wait_time': wait}
    sleep(wait)
    return x / y
