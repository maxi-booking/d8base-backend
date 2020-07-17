"""The managers tests module."""
from typing import List

import pytest
from cities.models import Country
from django.db.models.query import QuerySet

from contacts.models import Contact

pytestmark = pytest.mark.django_db


def test_contact_manager_get_by_country(
    countries: List[Country],
    contacts: QuerySet,
):
    """Should return a list of contacts filtered by the country."""
    result0 = Contact.objects.get_by_country(countries[0])

    assert contacts.count() != result0.count()
    assert result0[0].name == "icq"
    assert result0[1].name == "telegram"

    result1 = Contact.objects.get_by_country(countries[1])

    assert result0.count() != result1.count()
    assert result1[0].name == "whatsapp"
