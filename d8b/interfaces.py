"""The d8b interfaces module."""
from django.db import models


class AbstractDefaultEntry():
    """The absctract class with default field."""

    is_default: bool
    objects: models.Manager
