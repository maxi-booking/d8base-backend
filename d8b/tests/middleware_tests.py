"""The middleware tests module."""
import pytest
from django.urls import reverse

from d8b.middleware import ThreadSafeUserMiddleware

pytestmark = pytest.mark.django_db


def test_thread_safe_user_middleware(admin, admin_client):
    """Should save the request user in a thread safe local variable."""
    assert ThreadSafeUserMiddleware.get_current_user() is None
    response = admin_client.get(reverse('admin:users_user_changelist'))

    assert response.status_code == 200
    assert ThreadSafeUserMiddleware.get_current_user() == admin
