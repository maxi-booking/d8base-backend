"""The users repositories module."""

from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauthlib import common

from users.models import User


class OauthRepository():
    """The Oauth repository."""

    jwt_app_name: str = settings.JWT_APPLICATION_NAME
    token_expire: int = settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']
    jwt_app: Application

    def __init__(self) -> None:
        """Construct the object."""
        try:
            self.jwt_app = Application.objects.get(name=self.jwt_app_name)
        except Application.DoesNotExist:
            self.jwt_app = self.create_jwt_app()

    def create_jwt_app(self) -> Application:
        """Create a jwt application."""
        app = Application()
        app.name = self.jwt_app_name
        app.client_type = Application.CLIENT_CONFIDENTIAL
        app.authorization_grant_type = Application.GRANT_PASSWORD
        app.save()

        return app

    def create_access_token(self, user: User) -> AccessToken:
        """Create an access token."""
        expires = timezone.now() + timedelta(seconds=self.token_expire)
        access_token = AccessToken(
            user=user,
            scope='read write groups',
            expires=expires,
            token=common.generate_token(),
            application=self.jwt_app,
        )
        access_token.save()

        return access_token

    def create_refresh_token(
            self,
            access_token: AccessToken,
    ) -> RefreshToken:
        """Create a refresh token."""
        refresh_token = RefreshToken(
            user=access_token.user,
            token=common.generate_token(),
            application=self.jwt_app,
            access_token=access_token,
        )
        refresh_token.save()

        return refresh_token
