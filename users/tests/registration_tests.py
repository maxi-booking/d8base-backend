"""The registration tests module."""
import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from oauth2_provider.models import Application

from users.models import User
from users.registration import get_auth_tokens
from users.urls import get_urls

pytestmark = pytest.mark.django_db


def test_get_registration_urls():
    """Should return the filtered registration URLs."""
    names = [u.name for u in get_urls()]

    assert 'login' not in names
    assert 'logout' not in names
    assert 'register' in names
    assert len(names) == 10


def test_get_auth_tokens(user: User, client: Client):
    """Should return the correct auth tokens."""
    access, refresh = get_auth_tokens(user)
    app = Application.objects.get(name=settings.JWT_APPLICATION_NAME)

    assert client.get(reverse('api-root')).status_code == 401
    assert access is not None
    assert refresh is not None
    assert access.token != refresh.token
    assert client.get(
        reverse('api-root'),
        HTTP_AUTHORIZATION=f'Bearer {access.token}',
    ).status_code == 200
    assert client.get(
        reverse('api-root'),
        HTTP_AUTHORIZATION=f'Bearer {access.token}',
    ).status_code == 200

    response = client.post(
        reverse('oauth2_provider:token'),
        {
            'grant_type': 'refresh_token',
            'refresh_token': refresh.token,
            'client_id': app.client_id,
            'client_secret': app.client_secret,
        },
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.json()['access_token'] != access.token
