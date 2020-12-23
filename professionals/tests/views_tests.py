"""The views tests module."""
import pytest
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse
from django.utils.text import slugify
from pytest_mock import MockFixture

from conftest import OBJECTS_TO_CREATE
from d8b.lang import select_locale
from users.models import User

pytestmark = pytest.mark.django_db


def test_category_list(client: Client, categories: QuerySet):
    """Should return a list of categories."""
    response = client.get(reverse("categories-list"))

    assert response.status_code == 200
    assert response.accepted_media_type == "application/json"
    assert response.json()["count"] == categories.count()


def test_category_display(client: Client, categories: QuerySet):
    """Should return a list of categories."""
    cat = categories.first()
    response = client.get(reverse("categories-detail", args=[cat.pk]))

    assert response.status_code == 200
    assert response.accepted_media_type == "application/json"
    assert response.json()["name"] == cat.name_en


def test_category_display_de(client: Client, categories: QuerySet):
    """Should return a list of categories [de]."""
    cat = categories.first()
    with select_locale("de"):
        response = client.get(reverse("categories-detail", args=[cat.pk]))

    assert response.json()["name"] == cat.name_de
    assert response.json()["description"] == cat.description_de


def test_subcategory_list(client: Client, subcategories: QuerySet):
    """Should return a list of subcategories."""
    subcat = subcategories.first()
    response = client.get(reverse("subcategories-list"))

    assert response.status_code == 200
    assert response.accepted_media_type == "application/json"
    assert response.json()["count"] == subcategories.count()
    assert response.json()["results"][0]["name"] == "category 0: subcategory 0"
    assert response.json()["results"][0]["category"] == subcat.category.pk


def test_user_professionals_list(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should return a professionals list."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.get(reverse("user-professionals-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 2
    assert data["results"][0]["name"] == obj.name


def test_user_professionals_detail(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should return a user professional."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.get(
        reverse("user-professionals-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["level"] == obj.level


def test_user_professionals_generate_calendar(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
    mocker: MockFixture,
):
    """Should return a user professional."""
    mock = mocker.patch("professionals.views.generate_for_professional")
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse("user-professionals-generate-calendar", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "ok"
    mock.assert_called_once_with(professional=obj)


def test_user_professionals_detail_restricted_entry(
    admin: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professionals.filter(user=admin).first()
    response = client_with_token.get(
        reverse("user-professionals-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professionals_create(
    user: User,
    client_with_token: Client,
    subcategories: QuerySet,
):
    """Should be able to create a user professional object."""
    response = client_with_token.post(
        reverse("user-professionals-list"),
        {
            "name": "test professional",
            "description": "test professional description",
            "subcategory": subcategories.first().pk
        },
    )
    assert response.status_code == 201
    assert user.professionals.first().name == "test professional"


def test_user_professionals_update(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to update a user professional."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.patch(
        reverse("user-professionals-detail", args=[obj.pk]),
        {
            "name": "new name",
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.name == "new name"
    assert obj.user == user
    assert obj.modified_by == user


def test_user_professionals_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professionals.filter(user=admin).first()
    response = client_with_token.post(
        reverse("user-professionals-detail", args=[obj.pk]), {"name": "xxx"})
    assert response.status_code == 405


def test_user_professionals_delete(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to delete a user professionals."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.delete(
        reverse("user-professionals-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert professionals.filter(pk=obj.pk).count() == 0


def test_user_professionals_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professionals.filter(user=admin).first()
    response = client_with_token.delete(
        reverse("user-professionals-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_tags_list(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should return a professional tags list."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.get(reverse("user-professional-tags-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == OBJECTS_TO_CREATE * 2
    assert data["results"][0]["name"] == obj.name


def test_user_professional_tags_detail(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should return a user professional tag."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-tags-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == obj.name


def test_user_professional_tags_detail_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_tags.filter(professional__user=admin).first()
    response = client_with_token.get(
        reverse("user-professional-tags-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_tags_create(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional tag object."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse("user-professional-tags-list"),
        {
            "name": "test professional tag",
            "professional": obj.pk,
        },
    )
    assert response.status_code == 201
    assert obj.tags.first().name == "test professional tag"


def test_user_professional_tags_update(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should be able to update a user professional tag."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse("user-professional-tags-detail", args=[obj.pk]),
        {
            "name": "new name",
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.name == "new name"
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_tags_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_tags.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-professional-tags-detail", args=[obj.pk]), {"name": "x"})
    assert response.status_code == 405


def test_user_professional_tags_delete(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should be able to delete a user professional tag."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse("user-professional-tags-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert professional_tags.filter(pk=obj.pk).count() == 0


def test_user_professional_tags_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_tags.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse("user-professional-tags-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_professional_tags_list(
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should return a professional tag names list."""
    obj = professional_tags.order_by("name").first()
    response = client_with_token.get(reverse("professional-tags-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == OBJECTS_TO_CREATE * 4
    assert data["results"][0]["name"] == obj.name


def test_professional_photos_list(
    client_with_token: Client,
    professional_photos: QuerySet,
):
    """Should return a professional photos list."""
    obj = professional_photos.first()
    response = client_with_token.get(reverse("professional-photos-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == professional_photos.count()
    assert data["results"][0]["name"] == obj.name


def test_professional_photos_detail(
    client_with_token: Client,
    professional_photos: QuerySet,
):
    """Should return a professional photos detail."""
    obj = professional_photos.first()
    response = client_with_token.get(
        reverse("professional-photos-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == obj.name


def test_user_professional_contacts_list(
    user: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should return a professional contacts list."""
    obj = professional_contacts.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-contacts-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 4
    assert data["results"][0]["value"] == obj.value


def test_user_professional_contact_detail(
    user: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should return a user professional contact."""
    obj = professional_contacts.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-contacts-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["contact"] == obj.contact.pk


def test_user_professional_tags_contact_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_contacts.filter(professional__user=admin).first()
    response = client_with_token.get(
        reverse("user-professional-contacts-detail", args=[obj.pk]))
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
        reverse("user-professional-contacts-list"),
        {
            "value": "test professional contact",
            "contact": contacts[0].pk,
            "professional": obj.pk,
        },
    )
    assert response.status_code == 201
    assert obj.contacts.first().value == "test professional contact"


def test_user_professional_contacts_update(
    user: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should be able to update a user professional contact."""
    obj = professional_contacts.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse("user-professional-contacts-detail", args=[obj.pk]),
        {
            "value": "new name",
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.value == "new name"
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_contacts_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_contacts.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-professional-contacts-detail", args=[obj.pk]),
        {"name": "x"})
    assert response.status_code == 405


def test_user_professional_contacts_delete(
    user: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should be able to delete a user professional contact."""
    obj = professional_contacts.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse("user-professional-contacts-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert professional_contacts.filter(pk=obj.pk).count() == 0


def test_user_professional_contacts_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_contacts: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_contacts.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse("user-professional-contacts-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_locations_list(
    user: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should return a professional locations list."""
    obj = professional_locations.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-locations-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 4
    assert data["results"][0]["city"] == obj.city.pk


def test_user_professional_locations_detail(
    user: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should return a user professional location."""
    obj = professional_locations.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-locations-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["address"] == obj.address


def test_user_professional_location_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_locations.filter(professional__user=admin).first()
    response = client_with_token.patch(
        reverse("user-professional-locations-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_location_create(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional location object."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse("user-professional-locations-list"),
        {
            "address": "test address",
            "professional": obj.pk,
        },
    )
    assert response.status_code == 201
    assert obj.locations.first().address == "test address"


def test_user_professional_location_update(
    user: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should be able to update a user professional location."""
    obj = professional_locations.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse("user-professional-locations-detail", args=[obj.pk]),
        {
            "address": "new address",
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.address == "new address"
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_locations_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_locations.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-professional-locations-detail", args=[obj.pk]),
        {"name": "x"})
    assert response.status_code == 405


def test_user_professional_location_delete(
    user: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should be able to delete a user professional location."""
    obj = professional_locations.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse("user-professional-locations-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert professional_locations.filter(pk=obj.pk).count() == 0


def test_user_professional_locations_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_locations: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_locations.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse("user-professional-locations-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_professionals_list(
    client_with_token: Client,
    professionals: QuerySet,
    user_languages: QuerySet,
):
    """Should return a professionals list."""
    obj = professionals.filter().first()
    response = client_with_token.get(reverse("professionals-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 4
    entry = data["results"][0]
    assert entry["name"] == obj.name
    lang = user_languages.filter(user__pk=entry["user"]["id"]).first()
    assert entry["user"]["languages"][0]["language"] == lang.language


def test_professional_detail(
    client_with_token: Client,
    professionals: QuerySet,
    user_languages: QuerySet,
    professional_educations: QuerySet,
    professional_experience: QuerySet,
    professional_locations: QuerySet,
    professional_contacts: QuerySet,
    professional_tags: QuerySet,
):
    """Should return a user professional object."""
    obj = professionals.filter().first()
    response = client_with_token.get(
        reverse("professionals-detail", args=[obj.pk]))
    data = response.json()

    assert response.status_code == 200
    assert data["experience"] == obj.experience
    lang = user_languages.filter(user__pk=data["user"]["id"]).first()
    assert data["user"]["languages"][0]["language"] == lang.language
    assert len(data["educations"]) == professional_educations.filter(
        professional=obj).count()
    assert len(data["experience_entries"]) == professional_experience.filter(
        professional=obj).count()
    assert len(data["locations"]) == professional_locations.filter(
        professional=obj).count()
    assert len(data["contacts"]) == professional_contacts.filter(
        professional=obj).count()
    assert len(data["tags"]) == professional_tags.\
        filter(professional=obj).count()


def test_user_professional_education_list(
    user: User,
    client_with_token: Client,
    professional_educations: QuerySet,
):
    """Should return a professional education list."""
    obj = professional_educations.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-education-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 2
    assert data["results"][0]["deegree"] == obj.deegree


def test_user_professional_educations_detail(
    user: User,
    client_with_token: Client,
    professional_educations: QuerySet,
):
    """Should return a user professional education."""
    obj = professional_educations.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-education-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["university"] == obj.university


def test_user_professional_education_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_educations: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_educations.filter(professional__user=admin).first()
    response = client_with_token.patch(
        reverse("user-professional-education-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_education_create(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional education object."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse("user-professional-education-list"),
        {
            "university": "test university",
            "start_date": "2016-10-01",
            "professional": obj.pk,
        },
    )
    assert response.status_code == 201
    assert obj.educations.first().university == "test university"


def test_user_professional_education_update(
    user: User,
    client_with_token: Client,
    professional_educations: QuerySet,
):
    """Should be able to update a user professional education."""
    obj = professional_educations.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse("user-professional-education-detail", args=[obj.pk]),
        {
            "university": "new university",
            "start_date": "2010-10-01",
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.university == "new university"
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_education_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_educations: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_educations.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-professional-education-detail", args=[obj.pk]),
        {"university": "x"})
    assert response.status_code == 405


def test_user_professional_education_delete(
    user: User,
    client_with_token: Client,
    professional_educations: QuerySet,
):
    """Should be able to delete a user professional education."""
    obj = professional_educations.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse("user-professional-education-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert professional_educations.filter(pk=obj.pk).count() == 0


def test_user_professional_education_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_educations: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_educations.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse("user-professional-education-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_experience_list(
    user: User,
    client_with_token: Client,
    professional_experience: QuerySet,
):
    """Should return a professional experience list."""
    obj = professional_experience.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-experience-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 2
    assert data["results"][0]["company"] == obj.company


def test_user_professional_experience_detail(
    user: User,
    client_with_token: Client,
    professional_experience: QuerySet,
):
    """Should return a user professional experience."""
    obj = professional_experience.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-experience-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == obj.title


def test_user_professional_experience_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_experience: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_experience.filter(professional__user=admin).first()
    response = client_with_token.patch(
        reverse("user-professional-experience-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_experience_create(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional experience object."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse("user-professional-experience-list"),
        {
            "title": "test title",
            "company": "test company",
            "start_date": "2016-10-01",
            "professional": obj.pk,
        },
    )
    assert response.status_code == 201
    assert obj.experience_entries.first().company == "test company"


def test_user_professional_experience_update(
    user: User,
    client_with_token: Client,
    professional_experience: QuerySet,
):
    """Should be able to update a user professional experience."""
    obj = professional_experience.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse("user-professional-experience-detail", args=[obj.pk]),
        {
            "company": "new company",
            "start_date": "2016-11-01",
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.company == "new company"
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_experience_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_experience: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_experience.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-professional-experience-detail", args=[obj.pk]),
        {"title": "x"})
    assert response.status_code == 405


def test_user_professional_experience_delete(
    user: User,
    client_with_token: Client,
    professional_experience: QuerySet,
):
    """Should be able to delete a user professional experience."""
    obj = professional_experience.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse("user-professional-experience-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert professional_experience.filter(pk=obj.pk).count() == 0


def test_user_professional_experience_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_experience: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_experience.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse("user-professional-experience-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_certificate_list(
    user: User,
    client_with_token: Client,
    professional_certificates: QuerySet,
):
    """Should return a professional certificates list."""
    obj = professional_certificates.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-certificates-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 2
    assert data["results"][0]["organization"] == obj.organization


def test_user_professional_certificate_detail(
    user: User,
    client_with_token: Client,
    professional_certificates: QuerySet,
):
    """Should return a user professional certificates."""
    obj = professional_certificates.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-certificates-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == obj.name


def test_user_professional_certificate_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_certificates: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_certificates.filter(professional__user=admin).first()
    response = client_with_token.patch(
        reverse("user-professional-certificates-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_certificate_create(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional certificates object."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse("user-professional-certificates-list"),
        {
            "name":
                "test name",
            "organization":
                "test organization",
            "professional":
                obj.pk,
            "photo":
                ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKBAMAA"
                 "AB/HNKOAAAAGFBMVEXMzMyWlpajo6O3t7fFxcWcnJyxsbG+vr50Rsl6AAAAC"
                 "XBIWXMAAA7EAAAOxAGVKw4bAAAAJklEQVQImWNgwADKDAwsAQyuDAzMAgyMb"
                 "OYMAgyuLApAUhnMRgIANvcCBwsFJwYAAAAASUVORK5CYII=")
        },
    )
    certificate = obj.certificates.first()
    photo_path = f"certificates/{slugify(obj)}"
    assert response.status_code == 201
    assert certificate.name == "test name"
    assert photo_path in certificate.photo.name
    assert certificate.photo_thumbnail is not None
    certificate.photo.delete()


def test_user_professional_certificate_update(
    user: User,
    client_with_token: Client,
    professional_certificates: QuerySet,
):
    """Should be able to update a user professional certificates."""
    obj = professional_certificates.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse("user-professional-certificates-detail", args=[obj.pk]),
        {
            "organization": "new organization",
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.organization == "new organization"
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_certificates_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_certificates: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_certificates.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-professional-certificates-detail", args=[obj.pk]),
        {"title": "x"})
    assert response.status_code == 405


def test_user_professional_certificate_delete(
    user: User,
    client_with_token: Client,
    professional_certificates: QuerySet,
):
    """Should be able to delete a user professional certificates."""
    obj = professional_certificates.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse("user-professional-certificates-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert professional_certificates.filter(pk=obj.pk).count() == 0


def test_user_professional_certificates_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_certificates: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_certificates.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse("user-professional-certificates-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_photos_list(
    user: User,
    client_with_token: Client,
    professional_photos: QuerySet,
):
    """Should return a professional photos list."""
    obj = professional_photos.filter(professional__user=user).first()
    response = client_with_token.get(reverse("user-professional-photos-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 2
    assert data["results"][0]["name"] == obj.name


def test_user_professional_photo_detail(
    user: User,
    client_with_token: Client,
    professional_photos: QuerySet,
):
    """Should return a user professional photos."""
    obj = professional_photos.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-photos-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["description"] == obj.description


def test_user_professional_photos_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_photos: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_photos.filter(professional__user=admin).first()
    response = client_with_token.patch(
        reverse("user-professional-photos-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_photos_create(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional photos object."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse("user-professional-photos-list"),
        {
            "name":
                "test name",
            "description":
                "test description",
            "professional":
                obj.pk,
            "photo":
                ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKBAMAA"
                 "AB/HNKOAAAAGFBMVEXMzMyWlpajo6O3t7fFxcWcnJyxsbG+vr50Rsl6AAAAC"
                 "XBIWXMAAA7EAAAOxAGVKw4bAAAAJklEQVQImWNgwADKDAwsAQyuDAzMAgyMb"
                 "OYMAgyuLApAUhnMRgIANvcCBwsFJwYAAAAASUVORK5CYII=")
        },
    )
    photo = obj.photos.first()
    photo_path = f"photos/{slugify(obj)}"
    assert response.status_code == 201
    assert photo.name == "test name"
    assert photo_path in photo.photo.name
    assert photo.photo_thumbnail is not None
    photo.photo.delete()


def test_user_professional_photo_update(
    user: User,
    client_with_token: Client,
    professional_photos: QuerySet,
):
    """Should be able to update a user professional photos."""
    obj = professional_photos.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse("user-professional-photos-detail", args=[obj.pk]),
        {
            "name": "new name",
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.name == "new name"
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_photo_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_photos: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_photos.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-professional-photos-detail", args=[obj.pk]),
        {"name": "x"})
    assert response.status_code == 405


def test_user_professional_photo_delete(
    user: User,
    client_with_token: Client,
    professional_photos: QuerySet,
):
    """Should be able to delete a user professional photos."""
    obj = professional_photos.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse("user-professional-photos-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert professional_photos.filter(pk=obj.pk).count() == 0


def test_user_professional_photo_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_photos: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_photos.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse("user-professional-photos-detail", args=[obj.pk]))
    assert response.status_code == 404
