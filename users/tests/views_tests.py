"""The views tests module."""
import re
from typing import List
from urllib.parse import parse_qs, urlparse

import pytest
from cities.models import City, Country
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.query import QuerySet
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
            'first_name':
                'new_name',
            'email':
                'new_email@test.ru',
            'avatar':
                ('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKBAMAA'
                 'AB/HNKOAAAAGFBMVEXMzMyWlpajo6O3t7fFxcWcnJyxsbG+vr50Rsl6AAAAC'
                 'XBIWXMAAA7EAAAOxAGVKw4bAAAAJklEQVQImWNgwADKDAwsAQyuDAzMAgyMb'
                 'OYMAgyuLApAUhnMRgIANvcCBwsFJwYAAAAASUVORK5CYII=')
        },
        content_type='application/json',
    )
    admin.refresh_from_db()
    data = response.json()
    avatar_path = f'avatars/{ADMIN_EMAIL}'
    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert data['email'] == ADMIN_EMAIL
    assert data['first_name'] == 'new_name'
    assert admin.first_name == 'new_name'
    assert admin.email == ADMIN_EMAIL
    assert avatar_path in admin.avatar.name
    assert admin.avatar_thumbnail is not None
    admin.avatar.delete()


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
    groups = user.groups.all()
    assert user.first_name == 'test'
    assert user.check_password('test_pass')
    assert groups.count() == 1
    assert groups[0].name == settings.GROUP_USER_NAME


def test_user_languages_list(
    user: User,
    client_with_token: Client,
    user_languages: QuerySet,
):
    """Should return a languages list."""
    response = client_with_token.get(reverse('user-languages-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == user_languages.filter(user=user).count()
    assert data['results'][0]['language'] == 'fr'


def test_user_languages_detail(
    user: User,
    client_with_token: Client,
    user_languages: QuerySet,
):
    """Should return a user language."""
    lang = user_languages.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-languages-detail', args=[lang.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['language'] == lang.language


def test_user_languages_create(
    user: User,
    client_with_token: Client,
    user_languages: QuerySet,
):
    """Should be able to create a user language."""
    response = client_with_token.post(
        reverse('user-languages-list'),
        {
            'language': 'en',
            'is_native': False
        },
    )
    lang = user_languages.get(user=user, language='en')
    assert response.status_code == 201
    assert lang.is_native is False
    assert lang.user == user
    assert lang.created_by == user
    assert lang.modified_by == user


def test_user_languages_update(
    user: User,
    client_with_token: Client,
    user_languages: QuerySet,
):
    """Should be able to update a user language."""
    lang = user_languages.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-languages-detail', args=[lang.pk]),
        {
            'language': 'en',
            'is_native': True,
        },
    )
    lang.refresh_from_db()
    assert response.status_code == 200
    assert lang.is_native is True
    assert lang.language == 'en'
    assert lang.user == user
    assert lang.modified_by == user


def test_user_languages_delete(
    user: User,
    client_with_token: Client,
    user_languages: QuerySet,
):
    """Should be able to update a user language."""
    lang = user_languages.filter(user=user).first()
    response = client_with_token.delete(
        reverse('user-languages-detail', args=[lang.pk]))
    assert response.status_code == 204
    assert user_languages.filter(user=user).count() == 0


def test_user_locations_list(
    user: User,
    client_with_token: Client,
    user_locations: QuerySet,
):
    """Should return a locations list."""
    response = client_with_token.get(reverse('user-locations-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == user_locations.filter(user=user).count()

    assert data['results'][0]['address'] == 'test address 3'


def test_user_location_detail(
    user: User,
    client_with_token: Client,
    user_locations: QuerySet,
):
    """Should return a user location."""
    obj = user_locations.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-locations-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['city'] == obj.city.pk
    assert data['address'] == obj.address


def test_user_location_create(
    user: User,
    countries: List[Country],
    cities: List[City],
    client_with_token: Client,
    user_locations: QuerySet,
):
    """Should be able to create a user location."""
    response = client_with_token.post(
        reverse('user-locations-list'),
        {
            'address': 'new test address',
            'is_default': True,
            'city': cities[0].pk,
            'country': countries[0].pk
        },
    )
    obj = user_locations.get(user=user, address='new test address')

    assert response.status_code == 201
    assert obj.is_default is True
    assert obj.city == cities[0]
    assert obj.user == user
    assert obj.created_by == user
    assert obj.modified_by == user


def test_user_location_update(
    user: User,
    client_with_token: Client,
    user_locations: QuerySet,
):
    """Should be able to update a user location."""
    obj = user_locations.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-locations-detail', args=[obj.pk]),
        {
            'address': 'new test address',
            'is_default': True,
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.is_default is True
    assert obj.address == 'new test address'
    assert obj.user == user
    assert obj.modified_by == user


def test_user_location_delete(
    user: User,
    client_with_token: Client,
    user_locations: QuerySet,
):
    """Should be able to update a user language."""
    obj = user_locations.filter(user=user).first()
    response = client_with_token.delete(
        reverse('user-locations-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert user_locations.filter(user=user, pk=obj.pk).count() == 0
