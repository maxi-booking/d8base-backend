"""The routers tests module."""
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_swagger_url(client):
    """Should return a 200 HTTP response for authenticated users."""
    response = client.get(reverse('schema-swagger-ui'))

    assert response.status_code == 200


def test_redoc_url(client):
    """Should return a 200 HTTP response for authenticated users."""
    response = client.get(reverse('schema-redoc'))

    assert response.status_code == 200


def test_swagger_json(client):
    """Should return a JSON schema."""
    response = client.get(reverse('schema-json', kwargs={'format': '.json'}))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['info']['title'] == 'D8base API'


def test_swagger_yaml(client):
    """Should return a YAML schema."""
    response = client.get(reverse('schema-json', kwargs={'format': '.yaml'}))

    assert response.accepted_media_type == 'application/yaml'
    assert response.status_code == 200
    assert response.data['info']['title'] == 'D8base API'
