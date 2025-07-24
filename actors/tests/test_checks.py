from io import StringIO
from unittest.mock import patch

from django.core.management import call_command


def test_ldap_check_not_enabled():
    stderr = StringIO()
    call_command('check', '-t', 'compatibility', stderr=stderr)
    res = stderr.getvalue()
    assert res == ''


@patch('actors.apps.ldap', None)
@patch('actors.apps.settings.AUTHENTICATION_BACKENDS', ['django_auth_ldap.backend.LDAPBackend'])
def test_ldap_check():
    stderr = StringIO()
    call_command('check', '-t', 'compatibility', stderr=stderr)
    res = stderr.getvalue()
    assert '(ldap.E001) "django_auth_ldap" not available' in res
