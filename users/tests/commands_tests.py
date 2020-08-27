"""The commands test module."""
import pytest
from django.core.management import call_command

from users.models import User

pytestmark = pytest.mark.django_db


def test_update_user_group(user: User):
    """Should filter a queryset by user."""
    group = user.groups.first()
    group.permissions.clear()
    assert not group.permissions.count()
    call_command("update_user_group")
    assert group.permissions.count()
