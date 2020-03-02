"""The managers tests module."""
import pytest

from users.models import User

pytestmark = pytest.mark.django_db


def test_user_manager_create_user():
    """Should create a user."""
    user = User.objects.create_user(email='common@user.com', password='foo')

    assert user.email == 'common@user.com'
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    assert user.username is None
    with pytest.raises(TypeError):
        User.objects.create_user()  # type: ignore
    with pytest.raises(TypeError):
        User.objects.create_user(email='')  # type: ignore
    with pytest.raises(TypeError):
        User.objects.create_user(email='')  # type: ignore
    with pytest.raises(ValueError):
        User.objects.create_user(email='', password="foo")


def test_user_manager_create_superuser():
    """Should create a superuser."""
    user = User.objects.create_superuser('super@user.com', 'foo')

    assert user.email == 'super@user.com'
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser
    assert user.username is None

    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email='super@user.com',
            password='foo',
            is_superuser=False,
        )

    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email='super@user.com',
            password='foo',
            is_staff=False,
        )
