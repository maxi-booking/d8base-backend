"""The views tests module."""
from decimal import Decimal

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse
from django.utils.text import slugify
from moneyed import EUR, USD, Money

from services.models import Price, Service, ServiceTag
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


def test_user_service_prices_list(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should return a professional tags list."""
    # pylint: disable=unused-argument
    obj = Price.objects.filter(service__professional__user=user).first()
    response = client_with_token.get(reverse('user-service-prices-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 4
    price = data['results'][0]
    assert price['start_price'] == str(obj.start_price.amount)
    assert price['start_price_currency'] == str(obj.start_price.currency)
    assert price['payment_methods'] == ['cash', 'online']


def test_user_service_prices_detail(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should return a user professional tag."""
    # pylint: disable=unused-argument
    obj = Price.objects.filter(service__professional__user=user).first()
    response = client_with_token.get(
        reverse('user-service-prices-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['payment_methods'] == ['cash', 'online']


def test_user_service_prices_detail_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    # pylint: disable=unused-argument
    obj = Price.objects.filter(service__professional__user=admin).first()
    response = client_with_token.get(
        reverse('user-service-prices-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_service_prices_create(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to create a user professional tag object."""
    obj = services.filter(professional__user=user).first()
    obj.price.delete()
    response = client_with_token.post(
        reverse('user-service-prices-list'),
        {
            'price': 12.444,
            'is_price_fixed': True,
            'price_currency': 'EUR',
            'payment_methods': ['online', 'cash'],
            'service': obj.pk,
        },
    )
    assert response.status_code == 201
    obj.refresh_from_db()
    assert obj.price.price == Money(Decimal('12.444'), EUR)
    assert obj.price.payment_methods == ['online', 'cash']


def test_user_service_prices_update(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to update a user professional tag."""
    # pylint: disable=unused-argument
    obj = services.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse('user-service-prices-detail', args=[obj.price.pk]),
        {
            'price': 0.5,
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    price = obj.price
    assert price.price == Money(Decimal('0.5'), USD)
    assert price.service.professional.user == user
    assert price.modified_by == user


def test_user_service_prices_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    # pylint: disable=unused-argument
    obj = services.filter(professional__user=admin).first().price
    response = client_with_token.post(
        reverse('user-service-prices-detail', args=[obj.pk]), {'price': 1.5})
    assert response.status_code == 405


def test_user_service_prices_delete(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to delete a user professional tag."""
    # pylint: disable=unused-argument
    obj = services.filter(professional__user=user).first().price
    response = client_with_token.delete(
        reverse('user-service-prices-detail', args=[obj.pk]))
    assert response.status_code == 204

    with pytest.raises(ObjectDoesNotExist):
        _ = services.filter(professional__user=user).first().price


def test_user_service_prices_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    # pylint: disable=unused-argument
    obj = services.filter(professional__user=admin).first().price
    response = client_with_token.delete(
        reverse('user-service-prices-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_service_locations_list(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should return a professional tags list."""
    obj = services.filter(professional__user=user).first().locations.first()
    response = client_with_token.get(reverse('user-service-locations-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 2
    assert data['results'][0]['max_distance'] == obj.max_distance


def test_user_service_locations_detail(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should return a user professional tag."""
    obj = services.filter(professional__user=user).first().locations.first()
    response = client_with_token.get(
        reverse('user-service-locations-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['max_distance'] == obj.max_distance


def test_user_service_locations_detail_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    # pylint: disable=unused-argument
    obj = services.filter(professional__user=admin).first().locations.first()
    response = client_with_token.get(
        reverse('user-service-locations-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_service_locations_create(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to create a user professional tag object."""
    obj = services.filter(professional__user=user).first()
    obj.locations.all().delete()
    response = client_with_token.post(
        reverse('user-service-locations-list'),
        {
            'service': obj.pk,
            'max_distance': 4,
            'location': obj.professional.locations.first().pk,
        },
    )
    assert response.status_code == 201
    obj.refresh_from_db()
    assert obj.locations.first().max_distance == 4


def test_user_service_locations_update(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to update a user professional tag."""
    obj = services.filter(professional__user=user).first().locations.first()
    response = client_with_token.patch(
        reverse('user-service-locations-detail', args=[obj.pk]),
        {
            'max_distance': 0.5,
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.max_distance == Decimal('0.5')
    assert obj.service.professional.user == user
    assert obj.modified_by == user


def test_user_service_locations_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = services.filter(professional__user=admin).first().locations.first()
    response = client_with_token.post(
        reverse('user-service-locations-detail', args=[obj.pk]),
        {'max_distance': 1.5},
    )
    assert response.status_code == 405


def test_user_service_locations_delete(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to delete a user professional tag."""
    obj = services.filter(professional__user=user).first().locations.first()
    response = client_with_token.delete(
        reverse('user-service-locations-detail', args=[obj.pk]))
    assert response.status_code == 204

    assert not services.filter(
        professional__user=user).first().locations.count()


def test_user_service_locations_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = services.filter(professional__user=admin).first().locations.first()
    response = client_with_token.delete(
        reverse('user-service-locations-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_service_photos_list(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should return a professional tags list."""
    obj = services.filter(professional__user=user).first().photos.first()
    response = client_with_token.get(reverse('user-service-photos-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 4
    assert data['results'][0]['description'] == obj.description


def test_user_service_photos_detail(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should return a user professional tag."""
    obj = services.filter(professional__user=user).first().photos.first()
    response = client_with_token.get(
        reverse('user-service-photos-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == obj.name


def test_user_service_photos_detail_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = services.filter(professional__user=admin).first().photos.first()
    response = client_with_token.get(
        reverse('user-service-photos-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_service_photos_create(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to create a user professional tag object."""
    obj = services.filter(professional__user=user).first()
    obj.photos.all().delete()
    response = client_with_token.post(
        reverse('user-service-photos-list'),
        {
            'name':
                'test name',
            'description':
                'test description',
            'service':
                obj.pk,
            'photo':
                ('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKBAMAA'
                 'AB/HNKOAAAAGFBMVEXMzMyWlpajo6O3t7fFxcWcnJyxsbG+vr50Rsl6AAAAC'
                 'XBIWXMAAA7EAAAOxAGVKw4bAAAAJklEQVQImWNgwADKDAwsAQyuDAzMAgyMb'
                 'OYMAgyuLApAUhnMRgIANvcCBwsFJwYAAAAASUVORK5CYII=')
        },
    )
    assert response.status_code == 201
    obj.refresh_from_db()

    photo = obj.photos.first()
    photo_path = f'photos/{slugify(obj)}'
    assert response.status_code == 201
    assert photo.name == 'test name'
    assert photo_path in photo.photo.name
    assert photo.photo_thumbnail is not None
    photo.photo.delete()


def test_user_service_photos_update(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to update a user professional tag."""
    obj = services.filter(professional__user=user).first().photos.first()
    response = client_with_token.patch(
        reverse('user-service-photos-detail', args=[obj.pk]),
        {
            'name': 'new name',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.name == 'new name'
    assert obj.service.professional.user == user
    assert obj.modified_by == user


def test_user_service_photos_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = services.filter(professional__user=admin).first().photos.first()
    response = client_with_token.post(
        reverse('user-service-photos-detail', args=[obj.pk]),
        {'title': 'invalid'},
    )
    assert response.status_code == 405


def test_user_service_photos_delete(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to delete a user professional tag."""
    obj = services.filter(professional__user=user).first().photos.first()
    response = client_with_token.delete(
        reverse('user-service-photos-detail', args=[obj.pk]))
    assert response.status_code == 204

    assert not services.filter(professional__user=user).first().photos.count()


def test_user_service_photos_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = services.filter(professional__user=admin).first().photos.first()
    response = client_with_token.delete(
        reverse('user-service-photos-detail', args=[obj.pk]))
    assert response.status_code == 404
