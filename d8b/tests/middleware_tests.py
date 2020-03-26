"""The middleware tests module."""
import pytest
from django.test.client import Client
from django.urls import reverse

from d8b.middleware import ThreadSafeUserMiddleware
from users.models import User
from users.registration import get_auth_tokens

pytestmark = pytest.mark.django_db


def test_thread_safe_user_middleware(admin: User, admin_client: Client):
    """Should save the request user in a thread safe local variable."""
    assert ThreadSafeUserMiddleware.get_current_user() is None
    response = admin_client.get(reverse('admin:users_user_changelist'))

    assert response.status_code == 200
    assert ThreadSafeUserMiddleware.get_current_user() == admin


def test_thread_safe_user_middleware_token(user: User, client: Client):
    """Should save the request user in a thread safe local variable [token]."""
    assert client.get(reverse('api-root')).status_code == 401
    assert ThreadSafeUserMiddleware.get_current_user() is None

    access, _ = get_auth_tokens(user)

    assert client.get(
        reverse('api-root'),
        HTTP_AUTHORIZATION=f'Bearer {access.token}',
    ).status_code == 200

    assert ThreadSafeUserMiddleware.get_current_user() == user
