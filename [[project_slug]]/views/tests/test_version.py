import pytest
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_version_view(underprivileged_client):
    url = reverse('version')
    response = underprivileged_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'version': settings.VERSION}
