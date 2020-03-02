"""The d8b middleware module."""
from threading import local
from typing import Optional

from django.http.request import HttpRequest
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import activate

from users.models import User


class DisableAdminI18nMiddleware(MiddlewareMixin):
    """Disable the translation in the admin interface."""

    def process_request(self, request):
        """Set the locale to en in the admin interface."""
        # pylint: disable=unused-argument, no-self-use
        resolver_match = resolve(request.path)
        if resolver_match.app_name == 'admin':
            activate('en')


_USER = local()


class ThreadSafeUserMiddleware(MiddlewareMixin):
    """
    Store request's user into global thread-safe variable.

    Must be introduced AFTER
    `django.contrib.auth.middleware.AuthenticationMiddleware`.
    """

    def process_request(self, request: HttpRequest):
        """Set user."""
        # pylint: disable=unused-argument, no-self-use
        _USER.value = request.user

    @staticmethod
    def get_current_user() -> Optional[User]:
        """Return user."""
        if hasattr(_USER, 'value') and _USER.value:
            return _USER.value
        return None
