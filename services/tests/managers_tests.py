"""The managers tests module."""
import pytest
from django.db.models.query import QuerySet

from services.models import Service, ServiceTag

pytestmark = pytest.mark.django_db


def test_service_manager_get_user_list(services: QuerySet):
    """Should return the filtered list of services."""
    user = services[0].professional.user
    result = Service.objects.get_user_list(user)
    assert result.count() == 4
    assert not [r for r in result.all() if r.professional.user != user]


def test_servive_tag_manager_get_names(services: QuerySet):
    # pylint: disable=unused-argument
    """Should return the filtered list of service tags."""
    result = ServiceTag.objects.get_names()
    assert result.count() == ServiceTag.objects.\
        distinct("name").order_by("name").count()
    assert isinstance(result.first(), dict)
