"""The routers tests module."""
import pytest
from django.urls import reverse
from pytest_mock.plugin import MockFixture

from d8b.routers import DefaultRouter, get_router_urls

pytestmark = pytest.mark.django_db


def test_root_api_permissions(client):
    """Should return a 403 HTTP response for non-authenticated users."""
    response = client.get(reverse('api-root'))

    assert response.status_code == 401


def test_root_api(admin_client):
    """Should return a 200 HTTP response for authenticated users."""
    response = admin_client.get(reverse('api-root'))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'


def test_get_router_urls():
    """Should return a list of the router urls."""
    assert isinstance(get_router_urls(), list)


def test_router_extend(mocker: MockFixture):
    """Should extend the default router."""
    router = DefaultRouter()
    router.registry = ['one']

    arg1 = mocker.MagicMock()
    arg1.registry = ['two', 'three']

    arg2 = mocker.MagicMock()
    arg2.registry = ['four']

    router.extend(arg1, arg2)

    assert router.registry == ['one', 'two', 'three', 'four']
