import pytest
from django.contrib.auth.models import Permission

from actors import models

from . import factories


def test_user_representation():
    user = factories.UserFactory.build()
    assert str(user) == user.get_full_name()


@pytest.mark.django_db
def test_users_with_customers():
    factories.UserFactory.create_batch(5)
    factories.CustomerFactory.create_batch(5)
    user_1 = factories.UserFactory()
    factories.CustomerFactory(username=user_1.username)
    user_2 = factories.UserFactory()
    factories.CustomerFactory(username=user_2.username)
    user_qs = models.User.objects.filter(
        customer_id__isnull=False,  # filter users by existing customer (user.username == customer.username)
    ).order_by('pk')
    assert user_qs.count() == 2
    u1, u2 = user_qs
    assert u1.username == user_1.username
    assert u2.username == user_2.username


def test_customer_representation():
    customer = factories.CustomerFactory.build()
    assert str(customer) == customer.username


def test_group_permission_representation():
    gp = factories.GroupPermissionFactory.build(permission=Permission(id=1))
    assert str(gp) == f'{gp.pk} {gp.permission_id} {gp.group_id}'


def test_user_group_representation():
    ug = factories.UserGroupFactory.build()
    assert str(ug) == f'{ug.pk} {ug.user_id} {ug.group_id}'
