import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from actors.tests import factories


@pytest.mark.django_db
def test_user_group_list(api_client):
    ug = factories.UserGroupFactory()
    url = reverse('users-groups-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['results'][0]['id'] == ug.pk
    assert response.data['results'][0]['user'] == ug.user_id
    assert response.data['results'][0]['user_data']['id'] == ug.user_id
    assert response.data['results'][0]['group'] == ug.group_id
    assert response.data['results'][0]['group_data']['id'] == ug.group_id

@pytest.mark.django_db
def test_create_user_group(api_client):
    url = reverse('users-groups-list')
    user = factories.UserFactory()
    group = factories.GroupFactory()
    response = api_client.post(url, data={'user': user.id, 'group': group.id})
    assert response.status_code == status.HTTP_201_CREATED
    assert user.groups.count() == 1
    assert user.groups.first() == group

@pytest.mark.django_db
def test_bulk_create_user_group(api_client):
    url = reverse('users-groups-bulk-create')
    user_1, user_2 = factories.UserFactory.create_batch(2)
    group = factories.GroupFactory()
    data = [{'user': user_1.id, 'group': group.id}, {'user': user_2.id, 'group': group.id}]
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert group.user_set.count() == 2
