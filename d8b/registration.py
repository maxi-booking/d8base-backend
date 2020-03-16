"""The d8b registration module."""
from typing import List

from django.urls import URLPattern
from rest_registration.api.urls import urlpatterns

EXCLUDED_ROUTES = [
    'login', 'logout', 'verify-registration', 'register-email', 'verify-email'
]


def get_registration_urls() -> List[URLPattern]:
    """Return the registration urls."""
    return [u for u in urlpatterns if u.name not in EXCLUDED_ROUTES]
