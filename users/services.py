"""The users services module."""
from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist

if TYPE_CHECKING:
    from users.models import User


def get_user_public_last_name(user: "User") -> str:
    """Return the user name based on the user settings."""
    if not user.last_name:
        return ""
    try:
        is_hidden = user.settings.is_last_name_hidden
        return f"{user.last_name[0]}." if is_hidden else user.last_name
    except ObjectDoesNotExist:
        return user.last_name
