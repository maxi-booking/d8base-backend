"""The services documents tests module."""
import pytest
from django.db.models.query import QuerySet

from services.documents import ServiceDocument

pytestmark = pytest.mark.django_db


def test_service_document_prepare_tags(services: QuerySet):
    """Should return the service tags as a concatenated string."""
    service = services.first()
    assert ServiceDocument().prepare_tags(service) == "two one"


def test_service_document_prepare_professional_name(services: QuerySet):
    """Should return the professional name."""
    service = services.first()
    assert ServiceDocument().prepare_professional_name(
        service) == service.professional.name


def test_service_document_prepare_professional_description(services: QuerySet):
    """Should return the professional description."""
    service = services.first()
    assert ServiceDocument().prepare_professional_description(
        service) == service.professional.description


def test_service_document_prepare_professional_tags(
    services: QuerySet,
    professional_tags: QuerySet,
):
    """Should return the professional tags as a string."""
    # pylint: disable=unused-argument
    service = services.first()
    expected = " ".join([t.name for t in service.professional.tags.all()])
    assert ServiceDocument().prepare_professional_tags(service) == expected


def test_service_document_prepare_service_type(services: QuerySet):
    """Should return the service type."""
    service = services.first()
    assert ServiceDocument().prepare_service_type(
        service) == service.get_service_type_display()


def test_service_document_get_queryset(services: QuerySet):
    """Should return a queryset."""
    assert ServiceDocument().get_queryset().count() == services.count()
