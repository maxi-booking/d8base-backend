"""The setting getter module."""
from typing import Any

from django.conf import settings


def get_settings(name: str) -> Any:
    """Get settings by name."""
    return getattr(settings, name, None)
