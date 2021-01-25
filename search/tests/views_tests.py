"""The search engine getters tests module."""
import pytest
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db
# pylint: disable=protected-access


def test_search_list(client_with_token: Client, services: QuerySet):
    """Must return the search results list."""
    response = client_with_token.get(reverse("search-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == services.filter(is_enabled=True).count()
    pk = data["results"][0]["professional"]["id"]
    assert len(data["results"][0]["services"]) == services.filter(
        is_enabled=True, professional__pk=pk).count()


def test_search_list_filtered(client_with_token: Client, services: QuerySet):
    """Must return the search results list filtered by the query."""
    response = client_with_token.get(
        reverse("search-list") + "?query=professional")
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == services.filter(is_enabled=True).count()

    response = client_with_token.get(reverse("search-list") + "?query=invalid")
    data = response.json()
    assert response.status_code == 200
    assert not data["count"]

    response = client_with_token.get(reverse("search-list") + "?start_age=999")
    data = response.json()
    assert response.status_code == 200
    assert not data["count"]


def test_search_list_error(client_with_token: Client, services: QuerySet):
    """Must return the errors."""
    # pylint: disable=unused-argument
    response = client_with_token.get(
        reverse("search-list") + "?max_distance=0")
    data = response.json()
    assert response.status_code == 400
    assert "distance" in data["error"]
