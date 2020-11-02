"""The managers tests module."""
import pytest
from django.db.models.query import QuerySet

from services.models import Service, ServiceTag

pytestmark = pytest.mark.django_db


def test_services_manager_get_for_avaliability_generation(services: QuerySet):
    """Should return services by the ids."""
    first = services.filter(is_base_schedule=False).first()
    last = services.filter(is_base_schedule=False).last()
    ids = [first.pk, last.pk]
    services = Service.objects.get_for_avaliability_generation(ids)
    assert sorted(ids) == sorted([p.pk for p in services])


def test_services_manager_get_min_duration(services: QuerySet):
    """Should return a minimum duration."""
    professional = services.first().professional
    manager = Service.objects
    assert manager.get_min_duration(professional) == 60

    manager.update(is_enabled=True)
    service = services.filter(professional=professional).first()
    service.duration = 15
    service.save()
    assert manager.get_min_duration(professional) == 15

    manager.filter(professional=professional).delete()
    assert manager.get_min_duration(professional) == 0


def test_services_manager_get_by_params(services: QuerySet):
    """Should return a service."""
    expected = services.first()
    service = Service.objects.get_by_params(
        pk=expected.pk,
        name=expected.name,
    )
    assert service == expected
    assert Service.objects.get_by_params(pk=0) is None


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
