import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from actors.tests import factories


@pytest.mark.django_db
def test_user_list(api_client):
    url = reverse('users-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['results'][0]['id'] == api_client.user.pk


@pytest.mark.django_db
def test_user_detail(api_client):
    url = reverse('users-detail', kwargs={'pk': api_client.user.pk})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == api_client.user.pk


@pytest.mark.django_db
def test_get_current_user(api_client):
    url = reverse('users-me')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'password' not in response.data
    assert response.data['id'] == api_client.user.pk


@pytest.mark.django_db
def test_create_user(api_client):
    url = reverse('users-list')
    data = factories.UserFactory.as_dict()
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'password' not in response.data
    assert not response.data['has_password']


@pytest.mark.django_db
def test_set_user_password(api_client):
    url = reverse('users-my-password')
    new_pwd = '$tR0NgP4$$w0rD!'
    data = {'current_password': 'pwd', 'password': new_pwd}
    response = api_client.put(url, data=data)
    assert response.status_code == status.HTTP_200_OK
    api_client.user.refresh_from_db()
    assert api_client.user.check_password(new_pwd)


@pytest.mark.django_db
def test_set_user_password_current_error(api_client):
    url = reverse('users-my-password')
    data = {'current_password': 'bad', 'password': '123'}
    response = api_client.put(url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['current_password'] == ['Current password is incorrect']


@pytest.mark.django_db
def test_create_user_password_error(api_client):
    url = reverse('users-my-password')
    data = {'current_password': 'pwd', 'password': api_client.user.username + '_1'}
    response = api_client.put(url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['password'] == ['The password is too similar to the username.']


@pytest.mark.django_db
def test_group_users_list(api_client):
    ug = factories.UserGroupFactory()
    url = reverse('group-users-list', kwargs={'parent': ug.group_id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['results'][0]['id'] == ug.user_id


@pytest.mark.django_db
def test_group_users_add(api_client):
    ug = factories.UserGroupFactory()
    user_1, user_2 = factories.UserFactory.create_batch(2)
    url = reverse('group-users-list', kwargs={'parent': ug.group_id})
    response = api_client.post(url, data={'relations': [user_1.pk, user_2.pk]})
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.data) == 2
    assert ug.group.user_set.count() == 3
