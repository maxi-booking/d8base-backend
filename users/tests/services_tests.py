"""The commands test module."""
import pytest

from users.models import User, UserSettings
from users.services import get_user_public_last_name

pytestmark = pytest.mark.django_db


def test_get_user_public_last_name(user: User):
    """Should filter a queryset by user."""
    user.last_name = "Doe"
    assert get_user_public_last_name(user) == user.last_name

    settings = UserSettings()
    settings.user = user
    settings.is_last_name_hidden = False
    settings.save()
    assert get_user_public_last_name(user) == user.last_name

    settings.is_last_name_hidden = True
    settings.save()
    assert get_user_public_last_name(user) == "D."
