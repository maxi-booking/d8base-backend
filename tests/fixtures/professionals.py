"""The auth fixtures module."""

import pytest
from django.db.models.query import QuerySet

from conftest import OBJECTS_TO_CREATE
from professionals.models import (Category, Professional, ProfessionalContact,
                                  ProfessionalTag, Subcategory)
from users.models import User

# pylint: disable=redefined-outer-name


@pytest.fixture
def categories() -> QuerySet:
    """Return a categories queryset."""
    for i in range(0, OBJECTS_TO_CREATE):
        Category.objects.create(
            name_en=f'category {i}',
            description_en=f'category {i} description',
            name_de=f'kategorie {i}',
            description_de=f'kategorie {i} beschreibung',
        )
    return Category.objects.get_list()


@pytest.fixture
def subcategories(categories: QuerySet) -> QuerySet:
    """Return a categories queryset."""
    for category in categories:
        for i in range(0, 4):
            Subcategory.objects.create(
                category=category,
                name_en=f'{category}: subcategory {i}',
                description_en=f'{category}: subcategory {i} description',
                name_de=f'{category}: unterkategorie {i}',
                description_de='{category}: unterkategorie {i} beschreibung',
            )

    return Subcategory.objects.get_list()


@pytest.fixture
def professionals(
        subcategories: QuerySet,
        admin: User,
        user: User,
) -> QuerySet:
    """Return a professionals queryset."""
    for k, i in enumerate((
        (admin, Professional.LEVEL_JUNIOR, 0, subcategories[1]),
        (admin, Professional.LEVEL_MIDDLE, 3, subcategories[2]),
        (user, Professional.LEVEL_SENIOR, 12, subcategories[3]),
        (user, Professional.LEVEL_JUNIOR, 1, subcategories[4]),
    )):
        Professional.objects.create(
            user=i[0],
            name=f'professional {k}',
            description=f'professional description {k}',
            level=i[1],
            experience=i[2],
            subcategory=i[3],
        )
    return Professional.objects.get_list()


@pytest.fixture
def professional_tags(professionals: QuerySet, ) -> QuerySet:
    """Return a professional tags queryset."""
    for professional in professionals:
        for i in range(0, OBJECTS_TO_CREATE):
            ProfessionalTag.objects.create(
                professional=professional,
                name=f'tag {professional.pk}-{i}',
            )
    return ProfessionalTag.objects.get_list()


@pytest.fixture
def professional_contacts(professionals: QuerySet,
                          contacts: QuerySet) -> QuerySet:
    """Return a professional contacts queryset."""
    for professional in professionals:
        ProfessionalContact.objects.create(
            professional=professional,
            contact=contacts[0],
            value=f'{contacts[0]}',
        )
        ProfessionalContact.objects.create(
            professional=professional,
            contact=contacts[1],
            value=f'{contacts[0]}',
        )
    return ProfessionalContact.objects.get_list()
