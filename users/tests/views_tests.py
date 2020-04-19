"""The views tests module."""
import re
from typing import Any, Dict, List
from urllib.parse import parse_qs, urlparse

import pytest
from cities.models import City, Country
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse
from rest_framework.test import APIClient

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, USER_EMAIL, USER_PASSWORD
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


def _get_query_params_from_link_in_text(text: str) -> Dict[str, List[Any]]:
    """Find, parse a link and return query params."""
    pattern = re.compile((r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                          r'[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'))
    url = pattern.findall(text)[0]
    query_params = parse_qs(urlparse(url).query)

    return query_params


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
    query_params = _get_query_params_from_link_in_text(mailoutbox[0].body)

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


def _check_register_verification(
    client: Client,
    user: User,
    mailoutbox: List[EmailMultiAlternatives],
):
    """Verify a new user account."""
    assert len(mailoutbox) == 1
    query_params = _get_query_params_from_link_in_text(mailoutbox[0].body)

    response = client.post(
        reverse('verify-registration'),
        {
            'user_id': query_params['user_id'][0],
            'timestamp': query_params['timestamp'][0],
            'signature': query_params['signature'][0],
        },
        content_type='application/json',
    )
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.is_active
    assert user.is_confirmed


def test_accounts_register(
    client: Client,
    mailoutbox: List[EmailMultiAlternatives],
):
    """Should be able to register a new user."""
    expires: int = settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']
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
    assert response.json()['token']['access_token'] is not None
    assert response.json()['token']['refresh_token'] is not None
    assert response.json()['token']['scope'] == 'read write groups'
    assert response.json()['token']['token_type'] == 'Bearer'
    assert response.json()['token']['expires_in'] == expires

    user = User.objects.get(email='test@test.io')
    groups = user.groups.all()
    assert user.first_name == 'test'
    assert user.is_active
    assert not user.is_confirmed
    assert user.check_password('test_pass')
    assert groups.count() == 1
    assert groups[0].name == settings.GROUP_USER_NAME

    _check_register_verification(client, user, mailoutbox)


def test_resend_verify_registration(
    client_with_token: APIClient,
    client: Client,
    user: User,
    mailoutbox: List[EmailMultiAlternatives],
):
    """Should be able to resend a registration verification email."""
    response = client_with_token.post(reverse('resend-verify-registration'))

    assert response.status_code == 404
    user.is_confirmed = False
    user.save()

    client_with_token.post(reverse('resend-verify-registration'))

    _check_register_verification(client, user, mailoutbox)


def test_accounts_register_email(
    client_with_token: APIClient,
    user: User,
    mailoutbox: List[EmailMultiAlternatives],
):
    """Should be able to change a user email."""
    new_email = 'new_email@example.com'
    response = client_with_token.post(
        reverse('register-email'),
        {'email': new_email},
    )
    assert response.status_code == 200

    assert user.email == USER_EMAIL

    assert len(mailoutbox) == 1
    query_params = _get_query_params_from_link_in_text(mailoutbox[0].body)

    response = client_with_token.post(
        reverse('verify-email'),
        {
            'user_id': query_params['user_id'][0],
            'email': query_params['email'][0],
            'timestamp': query_params['timestamp'][0],
            'signature': query_params['signature'][0],
        },
    )
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.email == new_email
    assert user.is_confirmed


def test_user_languages_list(
    user: User,
    client_with_token: APIClient,
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
    """Should be able to delete a user language."""
    obj = user_locations.filter(user=user).first()
    response = client_with_token.delete(
        reverse('user-locations-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert user_locations.filter(user=user, pk=obj.pk).count() == 0


def test_user_contacts_list(
    user: User,
    client_with_token: Client,
    user_contacts: QuerySet,
):
    """Should return an contacts list."""
    response = client_with_token.get(reverse('user-contacts-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == user_contacts.filter(user=user).count()

    assert data['results'][0]['value'] == 'test contact 3'


def test_user_contacts_detail(
    user: User,
    client_with_token: Client,
    user_contacts: QuerySet,
):
    """Should return a user contact."""
    obj = user_contacts.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-contacts-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['value'] == obj.value
    assert data['contact'] == obj.contact.pk


def test_user_contacts_create(
    user: User,
    client_with_token: Client,
    user_contacts: QuerySet,
):
    """Should be able to create a user contact."""
    response = client_with_token.post(
        reverse('user-contacts-list'),
        {
            'value': 'test 123456',
            'contact': user_contacts[0].contact.pk
        },
    )
    obj = user_contacts.get(user=user, value='test 123456')

    assert response.status_code == 201
    assert obj.user == user
    assert obj.created_by == user
    assert obj.modified_by == user


def test_user_contacts_update(
    user: User,
    client_with_token: Client,
    user_contacts: QuerySet,
):
    """Should be able to update a user contact."""
    obj = user_contacts.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-contacts-detail', args=[obj.pk]),
        {
            'value': 'new test contact',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.value == 'new test contact'
    assert obj.user == user
    assert obj.modified_by == user


def test_user_contacts_delete(
    user: User,
    client_with_token: Client,
    user_contacts: QuerySet,
):
    """Should be able to delete a user contact."""
    obj = user_contacts.filter(user=user).first()
    response = client_with_token.delete(
        reverse('user-contacts-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert user_contacts.filter(user=user, pk=obj.pk).count() == 0


def test_user_settings_list(
    user: User,
    client_with_token: Client,
    user_settings: QuerySet,
):
    """Should return a settings list."""
    obj = user_settings.filter(user=user).first()
    response = client_with_token.get(reverse('user-settings-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['results'][0]['language'] == obj.language


def test_user_settings_detail(
    user: User,
    client_with_token: Client,
    user_settings: QuerySet,
):
    """Should return a user settings."""
    obj = user_settings.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-settings-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['currency'] == obj.currency


def test_user_settings_create(
    user: User,
    client_with_token: Client,
):
    """Should be able to create a user settings object."""
    response = client_with_token.post(
        reverse('user-settings-list'),
        {
            'language': 'de',
            'currency': 'EUR'
        },
    )
    assert response.status_code == 201
    assert user.settings.language == 'de'
    assert user.settings.currency == 'EUR'


def test_user_settings_update(
    user: User,
    client_with_token: Client,
    user_settings: QuerySet,
):
    """Should be able to update a user settings."""
    obj = user_settings.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-settings-detail', args=[obj.pk]),
        {
            'language': 'ru',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.language == 'ru'
    assert obj.user == user
    assert obj.modified_by == user


def test_user_settings_delete(
    user: User,
    client_with_token: Client,
    user_settings: QuerySet,
):
    """Should be able to delete a user settings."""
    obj = user_settings.filter(user=user).first()
    response = client_with_token.delete(
        reverse('user-settings-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert user_settings.filter(user=user).count() == 0
