from io import StringIO

import pytest
from django.core.management import call_command

from actors.models import User


@pytest.mark.django_db
def test_export_dashboards():
    out = StringIO()
    call_command('populate_db', '-s', 'test_superuser', stdout=out)
    res = out.getvalue()
    assert 'SUCCESS' in res
    assert User.objects.filter(username='test_superuser', is_superuser=True).count() == 1
