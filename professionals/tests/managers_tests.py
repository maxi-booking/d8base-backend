"""The managers tests module."""
import pytest
from django.db.models.query import QuerySet

from professionals.models import (Professional, ProfessionalLocation,
                                  ProfessionalTag)

pytestmark = pytest.mark.django_db


def test_professional_manager_get_for_avaliability_generation(
        professionals: QuerySet):
    """Should return professionals by the ids."""
    first = professionals.first()
    last = professionals.last()
    ids = [first.pk, last.pk]
    professionals = Professional.objects.get_for_avaliability_generation(ids)
    assert sorted(ids) == sorted([p.pk for p in professionals])


def test_professional_manager_get_by_params(professionals: QuerySet):
    """Should return a professional."""
    expected = professionals.first()
    professional = Professional.objects.get_by_params(
        pk=expected.pk,
        name=expected.name,
    )
    assert professional == expected
    assert Professional.objects.get_by_params(pk=0) is None


def test_professional_manager_get_user_list(professionals: QuerySet):
    """Should return the filtered list of professionals."""
    user = professionals[0].user
    result = Professional.objects.get_user_list(user)
    assert result.count() == 2
    assert not [r for r in result.all() if r.user != user]


def test_professional_location_manager_get_user_list(
        professional_locations: QuerySet):
    """Should return the filtered list of professional locations."""
    user = professional_locations[0].professional.user
    result = ProfessionalLocation.objects.get_user_list(user)
    assert result.count() == 4
    assert not [r for r in result if r.professional.user != user]


def test_professional_tag_manager_get_names(professional_tags: QuerySet):
    """Should return the filtered list of professionals."""
    result = ProfessionalTag.objects.get_names()
    assert result.count() == professional_tags.count()
    assert isinstance(result.first(), dict)
