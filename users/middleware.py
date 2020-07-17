"""The users middleware module."""

from typing import Optional

from django.http.request import HttpRequest
from django.utils import timezone
from pytz import UnknownTimeZoneError

from .models import User, UserLocation


class UserTimezoneMiddleware:
    """The user timezone middleware."""

    TIME_ZONE_HEADER = "HTTP_X_TIMEZONE"

    def __init__(self, get_response):
        """Construct the object."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        """Set the current user timezone."""
        user: User = request.user
        header = request.META.get(self.TIME_ZONE_HEADER)
        user_timezone: Optional[str] = None
        timezone.deactivate()
        if user.is_authenticated:
            user_timezone = UserLocation.objects.get_user_timezone(user)
        user_timezone = user_timezone or header

        if user_timezone:
            try:
                timezone.activate(user_timezone)
            except UnknownTimeZoneError:
                pass
        response = self.get_response(request)
        timezone.deactivate()
        return response
