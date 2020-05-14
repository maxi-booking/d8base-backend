"""The views tests module."""
import pytest
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse

from conftest import OBJECTS_TO_CREATE
from d8b.lang import select_locale
from users.models import User

pytestmark = pytest.mark.django_db


def test_category_list(client: Client, categories: QuerySet):
    """Should return a list of categories."""
    response = client.get(reverse('categories-list'))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['count'] == categories.count()


def test_category_display(client: Client, categories: QuerySet):
    """Should return a list of categories."""
    cat = categories.first()
    response = client.get(reverse('categories-detail', args=[cat.pk]))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['name'] == cat.name_en


def test_category_display_de(client: Client, categories: QuerySet):
    """Should return a list of categories [de]."""
    cat = categories.first()
    with select_locale('de'):
        response = client.get(reverse('categories-detail', args=[cat.pk]))

    assert response.json()['name'] == cat.name_de
    assert response.json()['description'] == cat.description_de


def test_subcategory_list(client: Client, subcategories: QuerySet):
    """Should return a list of subcategories."""
    subcat = subcategories.first()
    response = client.get(reverse('subcategories-list'))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['count'] == subcategories.count()
    assert response.json()['results'][0]['name'] == 'category 0: subcategory 0'
    assert response.json()['results'][0]['category'] == subcat.category.pk


def test_user_professionals_list(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should return a professionals list."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.get(reverse('user-professionals-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 2
    assert data['results'][0]['name'] == obj.name


def test_user_professionals_detail(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should return a user professional."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.get(
        reverse('user-professionals-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['level'] == obj.level


def test_user_professionals_detail_restricted_entry(
    admin: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professionals.filter(user=admin).first()
    response = client_with_token.get(
        reverse('user-professionals-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_professionals_create(
    user: User,
    client_with_token: Client,
    subcategories: QuerySet,
):
    """Should be able to create a user professional object."""
    response = client_with_token.post(
        reverse('user-professionals-list'),
        {
            'name': 'test professional',
            'description': 'test professional description',
            'subcategory': subcategories.first().pk
        },
    )
    assert response.status_code == 201
    assert user.professionals.first().name == 'test professional'


def test_user_professionals_update(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to update a user professional."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-professionals-detail', args=[obj.pk]),
        {
            'name': 'new name',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.name == 'new name'
    assert obj.user == user
    assert obj.modified_by == user


def test_user_professionals_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professionals.filter(user=admin).first()
    response = client_with_token.post(
        reverse('user-professionals-detail', args=[obj.pk]), {'name': 'xxx'})
    assert response.status_code == 405


def test_user_professionals_delete(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to delete a user professionals."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.delete(
        reverse('user-professionals-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert professionals.filter(pk=obj.pk).count() == 0


def test_user_professionals_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professionals.filter(user=admin).first()
    response = client_with_token.delete(
        reverse('user-professionals-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_tags_list(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should return a professional tags list."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.get(reverse('user-professional-tags-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == OBJECTS_TO_CREATE * 2
    assert data['results'][0]['name'] == obj.name


def test_user_professional_tags_detail(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should return a user professional tag."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse('user-professional-tags-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == obj.name


def test_user_professional_tags_detail_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_tags.filter(professional__user=admin).first()
    response = client_with_token.get(
        reverse('user-professional-tags-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_tags_create(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional tag object."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse('user-professional-tags-list'),
        {
            'name': 'test professional tag',
            'professional': obj.pk,
        },
    )
    assert response.status_code == 201
    assert obj.tags.first().name == 'test professional tag'


def test_user_professional_tags_update(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should be able to update a user professional tag."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse('user-professional-tags-detail', args=[obj.pk]),
        {
            'name': 'new name',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.name == 'new name'
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_tags_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_tags.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse('user-professional-tags-detail', args=[obj.pk]), {'name': 'x'})
    assert response.status_code == 405


def test_user_professional_tags_delete(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should be able to delete a user professional tag."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse('user-professional-tags-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert professional_tags.filter(pk=obj.pk).count() == 0


def test_user_professional_tags_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_tags.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse('user-professional-tags-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_professional_tags_list(
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should return a professional tag names list."""
    obj = professional_tags.order_by('name').first()
    response = client_with_token.get(reverse('professional-tags-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == OBJECTS_TO_CREATE * 4
    assert data['results'][0]['name'] == obj.name


def test_user_professional_contacts_list(
    user: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should return a professional contacts list."""
    obj = professional_contacts.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse('user-professional-contacts-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 4
    assert data['results'][0]['value'] == obj.value


def test_user_professional_contact_detail(
    user: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should return a user professional contact."""
    obj = professional_contacts.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse('user-professional-contacts-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['contact'] == obj.contact.pk


def test_user_professional_tags_contact_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_contacts.filter(professional__user=admin).first()
    response = client_with_token.get(
        reverse('user-professional-contacts-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_contacts_create(
    user: User,
    client_with_token: Client,
    contacts: QuerySet,
    professionals: QuerySet,
):
    """Should be able to create a user professional contact object."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse('user-professional-contacts-list'),
        {
            'value': 'test professional contact',
            'contact': contacts[0].pk,
            'professional': obj.pk,
        },
    )
    assert response.status_code == 201
    assert obj.contacts.first().value == 'test professional contact'


def test_user_professional_contacts_update(
    user: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should be able to update a user professional contact."""
    obj = professional_contacts.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse('user-professional-contacts-detail', args=[obj.pk]),
        {
            'value': 'new name',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.value == 'new name'
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_contacts_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_contacts.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse('user-professional-contacts-detail', args=[obj.pk]),
        {'name': 'x'})
    assert response.status_code == 405


def test_user_professional_contacts_delete(
    user: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should be able to delete a user professional contact."""
    obj = professional_contacts.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse('user-professional-contacts-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert professional_contacts.filter(pk=obj.pk).count() == 0


def test_user_professional_contacts_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_contacts.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse('user-professional-contacts-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_locations_list(
    user: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should return a professional locations list."""
    obj = professional_locations.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse('user-professional-locations-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 4
    assert data['results'][0]['city'] == obj.city.pk


def test_user_professional_locations_detail(
    user: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should return a user professional location."""
    obj = professional_locations.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse('user-professional-locations-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['address'] == obj.address


def test_user_professional_tags_location_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_locations.filter(professional__user=admin).first()
    response = client_with_token.patch(
        reverse('user-professional-locations-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_location_create(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional location object."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse('user-professional-locations-list'),
        {
            'address': 'test address',
            'professional': obj.pk,
        },
    )
    assert response.status_code == 201
    assert obj.locations.first().address == 'test address'


def test_user_professional_location_update(
    user: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should be able to update a user professional location."""
    obj = professional_locations.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse('user-professional-locations-detail', args=[obj.pk]),
        {
            'address': 'new address',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.address == 'new address'
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_locations_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_locations.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse('user-professional-locations-detail', args=[obj.pk]),
        {'name': 'x'})
    assert response.status_code == 405


def test_user_professional_location_delete(
    user: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should be able to delete a user professional location."""
    obj = professional_locations.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse('user-professional-locations-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert professional_locations.filter(pk=obj.pk).count() == 0


def test_user_professional_locations_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_locations.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse('user-professional-locations-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_professionals_list(
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should return a professionals list."""
    obj = professionals.filter().first()
    response = client_with_token.get(reverse('professionals-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 4
    assert data['results'][0]['name'] == obj.name


def test_professional_detail(
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should return a user professional object."""
    obj = professionals.filter().first()
    response = client_with_token.get(
        reverse('professionals-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['experience'] == obj.experience
