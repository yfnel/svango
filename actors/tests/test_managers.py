import pytest

from actors import models

from . import factories


@pytest.mark.django_db
def test_user_group_as_group():
    ug = factories.UserGroupFactory()
    user_group = models.UserGroup.objects.all().as_group().first()
    assert user_group.name == ug.group.name


@pytest.mark.django_db
def test_user_group_as_user():
    ug = factories.UserGroupFactory()
    user_group = models.UserGroup.objects.all().as_user().first()
    assert user_group.first_name == ug.user.first_name


@pytest.mark.django_db
def test_user_add_proxy_group_id():
    ug_1, ug_2 = factories.UserGroupFactory.create_batch(2)
    user_1, user_2 = models.User.objects.order_by('pk').add_proxy_group_id([ug_2.group_id])
    assert user_1.proxy_group_id is None
    assert user_2.proxy_group_id == ug_2.pk


@pytest.mark.django_db
def test_group_add_proxy_user_id():
    ug_1, ug_2 = factories.UserGroupFactory.create_batch(2)
    group_1, group_2 = models.PermissionGroup.objects.order_by('pk').add_proxy_user_id([ug_2.user_id])
    assert group_1.proxy_user_id is None
    assert group_2.proxy_user_id == ug_2.pk
