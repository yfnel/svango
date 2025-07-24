try:  # pragma: no cover
    import ldap
    from django_auth_ldap.backend import LDAPBackend, _LDAPUser
except ImportError:  # pragma: no cover
    ldap = None  # pragma: no cover


from django.apps import AppConfig
from django.conf import settings
from django.core.checks import CheckMessage, Tags, register
from django.core.checks import Warning as Warn


class ActorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'actors'


def check_connection() -> list[CheckMessage]:  # pragma: no cover
    ldap_user = _LDAPUser(LDAPBackend(), '')
    base_dn = ldap_user.settings.USER_DN_TEMPLATE or ldap_user.settings.USER_SEARCH.base_dn
    try:
        ldap_user.connection.search_ext(base_dn, ldap.SCOPE_SUBTREE, sizelimit=1, timeout=5)
    except ldap.INVALID_CREDENTIALS:
        return [Warn('Invalid LDAP credentials', id='ldap.E002')]
    except ldap.SERVER_DOWN:
        return [Warn('LDAP server unavailable', id='ldap.E003')]
    return []


@register(Tags.compatibility)
def ldap_connection(app_configs, **kwargs) -> list[CheckMessage]:  # noqa: ARG001, ANN001, ANN003
    if 'django_auth_ldap.backend.LDAPBackend' not in settings.AUTHENTICATION_BACKENDS:
        return []
    if not ldap:
        return [
            Warn('"django_auth_ldap" not available',
                 hint='install django_auth_ldap with poetry using flag "--with ldap".',
                 id='ldap.E001',
                 ),
        ]

    return check_connection()  # pragma: no cover
