"""The pytest fixtures module."""
import pytest
from django.test.client import Client

from users.models import User

collect_ignore_glob = ["*/migrations/*"]  # pylint: disable=invalid-name


@pytest.fixture()
def admin_client(db, admin_user) -> Client:
    """Return a Django test client logged in as an admin user."""
    client = Client()
    client.login(username=admin_user.email, password="admin_password")

    return client


@pytest.fixture
def admin() -> User:
    """Return an admin user."""
    return User.objects.create_superuser('admin@example.com', 'admin_password')


@pytest.fixture
def user() -> User:
    """Return a common user."""
    return User.objects.create_user('user@example.com', 'user_password')
