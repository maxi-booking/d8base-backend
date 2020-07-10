"""The views tests module."""
import pytest
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse

from services.models import Service, ServiceTag
from users.models import User

pytestmark = pytest.mark.django_db


def test_rates_list(
    client_with_token: Client,
    rates: QuerySet,
):
    """Should return a rates list."""
    obj = rates.order_by('currency').first()
    response = client_with_token.get(reverse('rates-list'))
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]['currency'] == obj.currency
    assert data[0]['value'] == str(obj.value)
    assert data[0]['title'] == 'Canadian Dollar'
    assert data[0]['sign'] == 'C$'
    assert 'CANADA' in data[0]['countries']
    assert data[1]['title'] == 'Euro'
    assert data[1]['sign'] == '€'
    assert 'FRANCE' in data[1]['countries']


def test_user_services_list(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should return a services list."""
    obj = services.filter(professional__user=user).first()
    response = client_with_token.get(reverse('user-services-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 4
    assert data['results'][0]['name'] == obj.name


def test_user_services_detail(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should return a user professional."""
    obj = services.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse('user-services-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['description'] == obj.description


def test_user_services_detail_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = services.filter(professional__user=admin).first()
    response = client_with_token.get(
        reverse('user-services-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_services_create(
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional object."""
    professional = professionals.first()
    response = client_with_token.post(
        reverse('user-services-list'),
        {
            'professional': professional.pk,
            'name': 'test service',
            'description': 'test professional description',
            'service_type': Service.TYPE_ONLINE,
            'duration': 15
        },
    )
    assert response.status_code == 201
    assert professional.services.first().name == 'test service'


def test_user_services_update(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to update a user professional."""
    obj = services.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse('user-services-detail', args=[obj.pk]),
        {
            'name': 'new name',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.name == 'new name'
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_services_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = services.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse('user-services-detail', args=[obj.pk]), {'name': 'xxx'})
    assert response.status_code == 405


def test_user_services_delete(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to delete a user services."""
    obj = services.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse('user-services-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert services.filter(pk=obj.pk).count() == 0


def test_user_services_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = services.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse('user-services-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_service_tags_list(
    client_with_token: Client,
    services: QuerySet,
):
    """Should return a service tag names list."""
    # pylint: disable=unused-argument
    obj = ServiceTag.objects.order_by('name').first()
    response = client_with_token.get(reverse('service-tags-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 3
    assert data['results'][0]['name'] == obj.name


def test_user_service_tags_list(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should return a professional tags list."""
    # pylint: disable=unused-argument
    obj = ServiceTag.objects.filter(service__professional__user=user).first()
    response = client_with_token.get(reverse('user-service-tags-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 10
    assert data['results'][0]['name'] == obj.name


def test_user_service_tags_detail(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should return a user professional tag."""
    # pylint: disable=unused-argument
    obj = ServiceTag.objects.filter(service__professional__user=user).first()
    response = client_with_token.get(
        reverse('user-service-tags-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == obj.name


def test_user_service_tags_detail_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    # pylint: disable=unused-argument
    obj = ServiceTag.objects.filter(service__professional__user=admin).first()
    response = client_with_token.get(
        reverse('user-service-tags-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_service_tags_create(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to create a user professional tag object."""
    obj = services.filter(professional__user=user).first()
    response = client_with_token.post(
        reverse('user-service-tags-list'),
        {
            'name': 'test services tag',
            'service': obj.pk,
        },
    )
    assert response.status_code == 201
    assert obj.tags.first().name == 'test services tag'


def test_user_service_tags_update(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to update a user professional tag."""
    # pylint: disable=unused-argument
    obj = ServiceTag.objects.filter(service__professional__user=user).first()
    response = client_with_token.patch(
        reverse('user-service-tags-detail', args=[obj.pk]),
        {
            'name': 'new name',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.name == 'new name'
    assert obj.service.professional.user == user
    assert obj.modified_by == user


def test_user_service_tags_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    # pylint: disable=unused-argument
    obj = ServiceTag.objects.filter(service__professional__user=admin).first()
    response = client_with_token.post(
        reverse('user-service-tags-detail', args=[obj.pk]), {'name': 'x'})
    assert response.status_code == 405


def test_user_service_tags_delete(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to delete a user professional tag."""
    # pylint: disable=unused-argument
    obj = ServiceTag.objects.filter(service__professional__user=user).first()
    response = client_with_token.delete(
        reverse('user-service-tags-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert ServiceTag.objects.filter(pk=obj.pk).count() == 0


def test_user_service_tags_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    # pylint: disable=unused-argument
    obj = ServiceTag.objects.filter(service__professional__user=admin).first()
    response = client_with_token.delete(
        reverse('user-service-tags-detail', args=[obj.pk]))
    assert response.status_code == 404


# prices
# locations
# photos
