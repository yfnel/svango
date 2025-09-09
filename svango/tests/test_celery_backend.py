import pytest
from celery import states

from svango.celery import app
from svango.celery_backend import SvangoCacheBackend


@pytest.fixture
def celery_backend():
    return SvangoCacheBackend(app=app)


def test_celery_backend(celery_backend, frozen_now):
    task_id = 'task_id'
    started_result = celery_backend.store_result(task_id, None, states.STARTED)
    assert started_result is None
    task_meta = celery_backend.get_task_meta(task_id)
    assert task_meta.get('date_start') == frozen_now.isoformat()
    assert task_meta.get('date_done') is None
    finished_result = celery_backend.store_result(task_id, 'OK', states.SUCCESS)
    assert finished_result == 'OK'
    task_meta = celery_backend.get_task_meta(task_id)
    assert task_meta.get('date_start') == frozen_now.isoformat()
    assert task_meta.get('date_done') == frozen_now.isoformat()
