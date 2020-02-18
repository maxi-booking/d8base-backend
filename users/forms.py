"""
The users forms module
"""
from typing import Tuple, Type

from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from .models import User


class UserCreationForm(BaseUserCreationForm):
    """
    The user create form
    """
    class Meta(BaseUserCreationForm):
        model: Type = User
        fields: Tuple[str] = ('email', )


class UserChangeForm(BaseUserChangeForm):
    """
    The user change form
    """
    class Meta:
        model: Type = User
        fields: Tuple[str] = ('email', )
