"""The location views test module."""
from typing import List

import pytest
from cities.models import City
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('route', [
    'continents-list',
    'countires-list',
    'regions-list',
    'subregions-list',
    'cities-list',
    'districts-list',
    'postal-codes-list',
    'alternative-names-list',
])
def test_api_endpoints(admin_client, route: str):
    """Should return the a JSON response."""
    response = admin_client.get(reverse(route))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'


def test_languages_list(admin_client):
    """Should return a list of languages."""
    response = admin_client.get(reverse('languages-list'))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    data = response.json()
    assert len(data) == len(settings.LANGUAGES)


def test_cities_list_filter(
    client_with_token: APIClient,
    cities: List[City],
):
    """Should return a filtered list of languages."""
    city = cities[0]
    city.name = 'test name'
    city.save()
    response = client_with_token.get(reverse('cities-list') + '?by_name=tes')
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['name'] == 'test name'


def test_languages_get(admin_client):
    """Should return a language object."""
    response = admin_client.get(reverse('languages-detail', args=['en']))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    data = response.json()
    assert data['code'] == 'en'
    assert data['name'] == 'English'

    response = admin_client.get(reverse('languages-detail', args=['invalid']))
    assert response.status_code == 404
