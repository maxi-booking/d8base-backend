"""The auth fixtures module."""

from typing import List

import arrow
import pytest
from cities.models import PostalCode
from django.db.models.query import QuerySet

from conftest import OBJECTS_TO_CREATE
from professionals.models import (Category, Professional,
                                  ProfessionalCertificate, ProfessionalContact,
                                  ProfessionalEducation,
                                  ProfessionalExperience, ProfessionalLocation,
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
def professional_contacts(
    professionals: QuerySet,
    contacts: QuerySet,
) -> QuerySet:
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
            value=f'{contacts[1]}',
        )
    return ProfessionalContact.objects.get_list()


@pytest.fixture
def professional_locations(
    professionals: QuerySet,
    postal_codes: List[PostalCode],
) -> QuerySet:
    """Return a professional locations queryset."""
    for professional in professionals:
        ProfessionalLocation.objects.create(
            professional=professional,
            postal_code=postal_codes[0],
            address=f'test address {postal_codes[0]}',
        )
        ProfessionalLocation.objects.create(
            professional=professional,
            postal_code=postal_codes[1],
            address=f'test address {postal_codes[1]}',
        )
    return ProfessionalLocation.objects.get_list()


@pytest.fixture
def professional_educations(professionals: QuerySet) -> QuerySet:
    """Return a professional educations queryset."""
    for professional in professionals:
        ProfessionalEducation.objects.create(
            professional=professional,
            university=f'university_{professional.pk}',
            deegree=f'degree_{professional.pk}',
            field_of_study=f'field_of_study_{professional.pk}',
            description=f'description_{professional.pk}',
            start_date=arrow.utcnow().shift(days=-3).date(),
            end_date=arrow.utcnow().shift(days=-2).date(),
        )
    return ProfessionalEducation.objects.get_list()


@pytest.fixture
def professional_experience(professionals: QuerySet) -> QuerySet:
    """Return a professional experience queryset."""
    for professional in professionals:
        ProfessionalExperience.objects.create(
            professional=professional,
            title=f'title_{professional.pk}',
            company=f'company_{professional.pk}',
            description=f'description_{professional.pk}',
            start_date=arrow.utcnow().shift(days=-3).date(),
            end_date=arrow.utcnow().shift(days=-2).date(),
        )
    return ProfessionalExperience.objects.get_list()


@pytest.fixture
def professional_certificates(professionals: QuerySet) -> QuerySet:
    """Return a professional experience queryset."""
    for professional in professionals:
        ProfessionalCertificate.objects.create(
            professional=professional,
            name=f'title_{professional.pk}',
            organization=f'company_{professional.pk}',
            date=arrow.utcnow().shift(days=-3).date(),
            certificate_id=f'certificate_id_{professional.pk}',
            url=f'http://certificate.com//certificate_{professional.pk}',
        )
    return ProfessionalCertificate.objects.get_list()
