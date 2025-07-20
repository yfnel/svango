import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from actors.tests import factories


@pytest.mark.django_db
def test_group_list(api_client):
    group = factories.GroupFactory()
    url = reverse('groups-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['results'][0]['id'] == group.pk
    assert response.data['results'][0]['name'] == group.name


@pytest.mark.django_db
def test_create_group(api_client):
    url = reverse('groups-list')
    data = factories.GroupFactory.as_dict()
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_get_user_group_list(api_client):
    ug = factories.UserGroupFactory()
    url = reverse('user-groups-list', kwargs={'parent': ug.user_id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['results'][0]['id'] == ug.group_id

@pytest.mark.django_db
def test_user_groups_add(api_client):
    ug = factories.UserGroupFactory()
    group_1, group_2 = factories.GroupFactory.create_batch(2)
    url = reverse('user-groups-list', kwargs={'parent': ug.user_id})
    response = api_client.post(url, data={'relations': [group_1.pk, group_2.pk]})
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.data) == 2
    assert ug.user.groups.count() == 3


@pytest.mark.django_db
def test_user_groups_delete(api_client):
    user = factories.UserFactory()
    ug_1, ug_2 = factories.UserGroupFactory.create_batch(2, user=user)
    url = reverse('user-groups-detail', kwargs={'parent': user.pk, 'pk': ug_1.pk})
    response = api_client.delete(url, data={'relations': [ug_1.group_id, ug_2.group_id]})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.groups.count() == 1
    assert user.groups.first() == ug_2.group


@pytest.mark.django_db
def test_user_groups_unlink(api_client):
    user = factories.UserFactory()
    ug_1, ug_2, ug_3 = factories.UserGroupFactory.create_batch(3, user=user)
    url = reverse('user-groups-unlink', kwargs={'parent': user.pk})
    response = api_client.patch(url, data={'relations': [ug_1.group_id, ug_2.group_id]})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.groups.count() == 1
    assert user.groups.first() == ug_3.group

