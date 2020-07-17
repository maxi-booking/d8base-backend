"""The auth fixtures module."""
import pytest
from django.test.client import Client
from rest_framework.test import APIClient

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, USER_EMAIL, USER_PASSWORD
from d8b import middleware
from users.models import User
from users.registration import get_auth_tokens


# pylint: disable=redefined-outer-name
@pytest.fixture()
def admin_client(admin: User) -> Client:
    """Return a Django test client logged in as an admin user."""
    client = Client()
    client.login(username=admin.email, password=ADMIN_PASSWORD)

    return client


@pytest.fixture()
def client_with_token(user: User) -> APIClient:
    """Return a Django test client logged with a token."""
    client = APIClient()
    access, _ = get_auth_tokens(user)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access.token)

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
        is_confirmed=True,
    )


@pytest.fixture(autouse=True)
def before_all():
    """Run before all tests."""
    # pylint: disable=protected-access
    middleware._USER.value = None
