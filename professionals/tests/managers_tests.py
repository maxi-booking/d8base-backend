"""The filtersets tests module."""
import pytest
from django.db.models.query import QuerySet

from professionals.models import Professional, ProfessionalTag

pytestmark = pytest.mark.django_db


def test_professional_manager_get_user_list(professionals: QuerySet):
    """Should return the filtered list of professionals."""
    user = professionals[0].user
    result = Professional.objects.get_user_list(user)
    assert result.count() == 2
    assert len([r for r in result.all() if r.user == user]) == 2


def test_professional_tag_manager_get_names(professional_tags: QuerySet):
    """Should return the filtered list of professionals."""
    result = ProfessionalTag.objects.get_names()
    assert result.count() == professional_tags.count()
    assert isinstance(result.first(), dict)
