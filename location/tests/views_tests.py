"""The location views test module."""
import pytest
from django.conf import settings
from django.urls import reverse

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
