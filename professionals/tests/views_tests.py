"""The views tests module."""
import pytest
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse

from d8b.lang import select_locale

pytestmark = pytest.mark.django_db


def test_category_list(client: Client, categories: QuerySet):
    """Should return a list of categories."""
    response = client.get(reverse('categories-list'))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['count'] == categories.count()


def test_category_display(client: Client, categories: QuerySet):
    """Should return a list of categories."""
    cat = categories.first()
    response = client.get(reverse('categories-detail', args=[cat.pk]))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['name'] == cat.name_en


def test_category_display_de(client: Client, categories: QuerySet):
    """Should return a list of categories [de]."""
    cat = categories.first()
    with select_locale('de'):
        response = client.get(reverse('categories-detail', args=[cat.pk]))

    assert response.json()['name'] == cat.name_de
    assert response.json()['description'] == cat.description_de


def test_subcategory_list(client: Client, subcategories: QuerySet):
    """Should return a list of subcategories."""
    subcat = subcategories.first()
    response = client.get(reverse('subcategories-list'))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['count'] == subcategories.count()
    assert response.json()['results'][0]['name'] == 'category 0: subcategory 0'
    assert response.json()['results'][0]['category'] == subcat.category.pk
