"""The repositories tests module."""
import pytest
from django.conf import settings
from django.utils import timezone
from oauth2_provider.models import Application

from users.models import User
from users.repositories import GroupRepository, OauthRepository

pytestmark = pytest.mark.django_db


def test_group_repository_get_or_create_user_group():
    """Should create or return the users group."""
    repo = GroupRepository()
    group = repo.get_or_create_user_group()

    codenames = [p.codename for p in group.permissions.all()]
    assert sorted(codenames) == sorted(settings.GROUP_USER_PERMISSIONS)
    assert group == repo.get_or_create_user_group()
    assert group.name == settings.GROUP_USER_NAME


def test_oauth_repository_init():
    """Should create a repository instance."""
    assert Application.objects.all().count() == 0

    repo = OauthRepository()
    app = repo.jwt_app

    assert app is not None

    repo = OauthRepository()
    assert repo.jwt_app == app
    assert repo.jwt_app.client_id == app.client_id
    assert repo.jwt_app.client_secret == app.client_secret
    assert app.name == settings.JWT_APPLICATION_NAME
    assert Application.objects.all().count() == 1


def test_oauth_repository_create_access_token(user: User):
    """Should return an access token."""
    access_token = OauthRepository().create_access_token(user)
    assert access_token.scope == "read write groups"
    assert access_token.user == user
    assert access_token.token is not None
    assert access_token.expires > timezone.now()
    assert access_token.application.name == settings.JWT_APPLICATION_NAME


def test_oauth_repository_create_refresh_token(user: User):
    """Should return an refresh token."""
    repo = OauthRepository()
    access_token = repo.create_access_token(user)
    refresh_token = repo.create_refresh_token(access_token)
    assert refresh_token.access_token == access_token
    assert refresh_token.user == user
    assert refresh_token.token is not None
    assert refresh_token.application.name == settings.JWT_APPLICATION_NAME
