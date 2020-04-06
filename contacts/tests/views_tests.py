"""The views tests module."""
from typing import List

import pytest
from cities.models import Country
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_contacts_list(admin_client: Client, contacts: QuerySet):
    """Should return a list of contacts."""
    response = admin_client.get(reverse('contacts-list'))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['count'] == contacts.count()


def test_contacts_list_filtered(
    admin_client: Client,
    contacts: QuerySet,
    countries: List[Country],
):
    """Should return a filtered list of languages."""
    response = admin_client.get(
        reverse('contacts-list') + f'?by_country={countries[0].pk}')

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['count'] != contacts.count()
    assert response.json()['results'][0]['name'] == 'icq'
