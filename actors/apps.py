import importlib

from django.apps import AppConfig
from django.conf import settings
from django.core.checks import CheckMessage, Tags, register
from django.core.checks import Warning as Warn


class ActorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'actors'


@register(Tags.compatibility)
def ldap_requirements_check(app_configs, **kwargs) -> list[CheckMessage]:  # noqa: ARG001, ANN001, ANN003
    errors = []
    ldap_enabled = 'django_auth_ldap.backend.LDAPBackend' in settings.AUTHENTICATION_BACKENDS
    if ldap_enabled and not importlib.util.find_spec('django_auth_ldap'):
        errors.append(
            Warn(
                '"django_auth_ldap" not available',
                hint='install django_auth_ldap with poetry using flag "--with ldap".',
                obj=None,
                id='ldap.E001',
            ),
        )
    return errors
