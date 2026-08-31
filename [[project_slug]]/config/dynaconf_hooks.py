try:  # pragma: no cover
    from django_auth_ldap import config
except ImportError:  # pragma: no cover
    config = None


from dynaconf.hooking import HookableSettings


def post(settings: HookableSettings) -> dict:
    data = {'dynaconf_merge': True}
    if config:  # pragma: no cover
        data['AUTH_LDAP_USER_SEARCH'] = config.LDAPSearch(**settings.AUTH_LDAP_USER_SEARCH_PARAMS)
    return data
