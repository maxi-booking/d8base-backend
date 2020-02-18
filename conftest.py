"""
The pytest fixtures module
"""
import pytest

from users.models import User

collect_ignore_glob = ["*/migrations/*"]  # pylint: disable=invalid-name


@pytest.fixture
def admin() -> User:
    """
    Return an admin user
    """
    return User.objects.create_superuser('super@user.com', 'super_password')


@pytest.fixture
def user() -> User:
    """
    Return a common user
    """
    return User.objects.create_superuser('common@user.com', 'common_password')
