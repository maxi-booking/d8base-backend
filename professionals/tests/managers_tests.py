"""The managers tests module."""
import pytest
from django.db.models.query import QuerySet

from professionals.models import (Professional, ProfessionalLocation,
                                  ProfessionalTag)

pytestmark = pytest.mark.django_db


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
