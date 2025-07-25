import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from actors.models import UserPermission
from actors.tests.factories import UserFactory


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def api_client() -> APIClient:
    user = UserFactory(first_name='api', last_name='user')
    user.user_permissions.add(*UserPermission.objects.only('id'))
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    client.user = user
    return client
