from svango.celery import debug_task


def test_debug_task():
    res = debug_task.delay()
    assert res.state == 'SUCCESS'
