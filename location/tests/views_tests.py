"""The users admin test module."""
import pytest
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
