from svango.celery import debug_task


def test_debug_task():
    res = debug_task.delay(10, 5, 0)
    assert res.state == 'SUCCESS'
