"""The users urls module."""

from typing import List

from django.urls import URLPattern, re_path
from rest_registration.api.urls import urlpatterns

from .views import resend_verify_registration

EXCLUDED_ROUTES = ['login', 'logout']


def get_urls() -> List[URLPattern]:
    """Return the registration urls."""
    urlpatterns.append(
        re_path(
            'resend-verify-registration',
            resend_verify_registration,
            name='resend-verify-registration',
        ))
    return [u for u in urlpatterns if u.name not in EXCLUDED_ROUTES]
