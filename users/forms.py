"""The users forms module."""
from typing import Tuple, Type

from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from .models import User


class UserCreationForm(BaseUserCreationForm):
    """The user create form."""

    class Meta(BaseUserCreationForm):
        """The user create form [meta]."""

        model: Type = User
        fields: Tuple[str] = ("email", )


class UserChangeForm(BaseUserChangeForm):
    """The user change form."""

    class Meta:
        """The user change form [meta]."""

        model: Type = User
        fields: Tuple[str] = ("email", )
