from django_auth_ldap import config
from dynaconf.hooking import HookableSettings


def post(settings: HookableSettings) -> dict:
    data = {'dynaconf_merge': True}
    data['AUTH_LDAP_USER_SEARCH'] = config.LDAPSearch(**settings.AUTH_LDAP_USER_SEARCH_PARAMS)
    return data
