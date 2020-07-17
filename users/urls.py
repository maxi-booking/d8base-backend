"""The users urls module."""

from typing import List

from django.urls import URLPattern, re_path
from rest_registration.api.urls import urlpatterns

from .views import is_user_registered, resend_verify_registration

EXCLUDED_ROUTES = ["login", "logout"]


def get_urls() -> List[URLPattern]:
    """Return the registration urls."""
    urlpatterns.extend([
        re_path(
            "resend-verify-registration",
            resend_verify_registration,
            name="resend-verify-registration",
        ),
        re_path(
            "is-user-registered",
            is_user_registered,
            name="is-user-registered",
        ),
    ])
    return [u for u in urlpatterns if u.name not in EXCLUDED_ROUTES]
