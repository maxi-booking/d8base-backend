"""The users registration module."""
from typing import List, Tuple

from django.urls import URLPattern
from oauth2_provider.models import AccessToken, RefreshToken
from rest_registration.api.urls import urlpatterns

from users.models import User
from users.repositories import OauthRepository

EXCLUDED_ROUTES = [
    'login', 'logout', 'verify-registration', 'register-email', 'verify-email'
]


def get_registration_urls() -> List[URLPattern]:
    """Return the registration urls."""
    return [u for u in urlpatterns if u.name not in EXCLUDED_ROUTES]


def get_auth_tokens(user: User) -> Tuple[AccessToken, RefreshToken]:
    """Return refresh and auth tokens."""
    repo = OauthRepository()
    access_token = repo.create_access_token(user)
    refresh_token = repo.create_refresh_token(access_token)

    return access_token, refresh_token
