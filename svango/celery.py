import os

from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'svango.config.settings')

app = Celery('svango')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:  # noqa: ANN001
    msg = f'Request: {self.request!r}'
    logger.info(msg)
