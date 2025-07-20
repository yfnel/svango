from django.contrib.auth.models import Permission

from . import factories


def test_user_representation():
    user = factories.UserFactory.build()
    assert str(user) == user.get_full_name()


def test_group_permission_representation():
    gp = factories.GroupPermissionFactory.build(permission=Permission(id=1))
    assert str(gp) == f'{gp.pk} {gp.permission_id} {gp.group_id}'


def test_user_group_representation():
    ug = factories.UserGroupFactory.build()
    assert str(ug) == f'{ug.pk} {ug.user_id} {ug.group_id}'
