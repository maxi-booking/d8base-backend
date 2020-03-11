"""The pytest fixtures module."""
import pytest
from django.test.client import Client

from users.models import User

collect_ignore_glob = ['*/migrations/*']  # pylint: disable=invalid-name

ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'admin_password'
USER_EMAIL = 'user@example.com'
USER_PASSWORD = 'user_password'


# pylint: disable=redefined-outer-name
@pytest.fixture()
def admin_client(admin: User) -> Client:
    """Return a Django test client logged in as an admin user."""
    client = Client()
    client.login(username=admin.email, password=ADMIN_PASSWORD)

    return client


@pytest.fixture
def admin() -> User:
    """Return an admin user."""
    return User.objects.create_superuser(
        ADMIN_EMAIL,
        ADMIN_PASSWORD,
    )


@pytest.fixture
def user() -> User:
    """Return a common user."""
    return User.objects.create_user(
        USER_EMAIL,
        USER_PASSWORD,
    )
