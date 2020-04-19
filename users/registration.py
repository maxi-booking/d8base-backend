"""The users registration module."""
from typing import Tuple

from oauth2_provider.models import AccessToken, RefreshToken

from users.models import User
from users.repositories import OauthRepository


def get_auth_tokens(user: User) -> Tuple[AccessToken, RefreshToken]:
    """Return refresh and auth tokens."""
    repo = OauthRepository()
    access_token = repo.create_access_token(user)
    refresh_token = repo.create_refresh_token(access_token)

    return access_token, refresh_token
