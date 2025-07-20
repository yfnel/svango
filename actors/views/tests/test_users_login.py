from unittest.mock import ANY

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from actors.tests import factories


@pytest.mark.django_db
def test_login_user(client):
    data = {'username': 'username', 'password': 'secret'}
    user = factories.UserFactory(**data)
    response = client.post(reverse('users-login-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == user.username


@pytest.mark.django_db
def test_login_user_bad_password(client):
    data = {'username': 'username', 'password': 'secret'}
    factories.UserFactory(**data)
    data['password'] = 'bad'
    response = client.post(reverse('users-login-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_token_login(api_client):
    data = {'username': 'username', 'password': 'secret'}
    factories.UserFactory(**data)
    response = api_client.post(reverse('token-obtain'), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'access': ANY, 'refresh': ANY}
