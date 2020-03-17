"""The views tests module."""
import re
from typing import List
from urllib.parse import parse_qs, urlparse

import pytest
from django.core.mail import EmailMultiAlternatives
from django.test.client import Client
from django.urls import reverse

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, USER_PASSWORD
from users.models import User
from users.repositories import OauthRepository

pytestmark = pytest.mark.django_db


def test_auth_get_token(user: User, client: Client):
    """Should be able to login the user."""
    repo = OauthRepository()

    response = client.post(
        reverse('oauth2_provider:token'),
        {
            'grant_type': 'password',
            'username': user.email,
            'password': USER_PASSWORD,
            'client_id': repo.jwt_app.client_id,
            'client_secret': repo.jwt_app.client_secret,
        },
        content_type='application/json',
    )
    assert response.status_code == 200
    access = response.json()['access_token']

    assert client.get(
        reverse('api-root'),
        HTTP_AUTHORIZATION=f'Bearer {access}',
    ).status_code == 200


def test_accounts_profile_get(admin_client):
    """Should return the user profile."""
    response = admin_client.get(reverse('profile'))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['email'] == ADMIN_EMAIL


def test_accounts_profile_update(admin: User, admin_client: Client):
    """Should be able to update the user profile."""
    response = admin_client.patch(
        reverse('profile'),
        {
            'first_name': 'new_name',
            'email': 'new_email@test.ru',
        },
        content_type='application/json',
    )
    admin.refresh_from_db()
    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['email'] == ADMIN_EMAIL
    assert response.json()['first_name'] == 'new_name'
    assert admin.first_name == 'new_name'
    assert admin.email == ADMIN_EMAIL


def test_accounts_change_password(admin: User, admin_client: Client):
    """Should be able to change the user password."""
    response = admin_client.post(
        reverse('change-password'),
        {
            'old_password': ADMIN_PASSWORD,
            'password': 'new_password',
            'password_confirm': 'new_password',
        },
        content_type='application/json',
    )
    admin.refresh_from_db()
    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert admin.check_password('new_password')
    assert not admin.check_password(ADMIN_PASSWORD)


def test_accounts_reset_password(
    user: User,
    client: Client,
    mailoutbox: List[EmailMultiAlternatives],
):
    """Should be able to reset the user password."""
    response = client.post(
        reverse('send-reset-password-link'),
        {'login': user.email},
        content_type='application/json',
    )
    assert response.status_code == 200
    assert len(mailoutbox) == 1
    pattern = re.compile((r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                          r'[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'))
    url = pattern.findall(mailoutbox[0].body)[0]
    query_params = parse_qs(urlparse(url).query)

    response = client.post(
        reverse('reset-password'),
        {
            'user_id': query_params['user_id'][0],
            'timestamp': query_params['timestamp'][0],
            'signature': query_params['signature'][0],
            'password': 'new_password',
        },
        content_type='application/json',
    )
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.check_password('new_password')
    assert not user.check_password(USER_PASSWORD)


def test_accounts_register(client: Client):
    """Should be able to register a new user."""
    response = client.post(
        reverse('register'),
        {
            'email': 'test@test.io',
            'first_name': 'test',
            'password': 'test_pass',
            'password_confirm': 'test_pass',
        },
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.json()['token']['access'] is not None
    assert response.json()['token']['refresh'] is not None

    user = User.objects.get(email='test@test.io')
    assert user.first_name == 'test'
    assert user.check_password('test_pass')
