"""The users models module."""
from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """The user class."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = []

    objects: UserManager = UserManager()

    def __str__(self):
        """Return a string representation of the object."""
        return self.email
