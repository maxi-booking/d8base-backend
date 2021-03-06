"""The professionals managers module."""
from typing import TYPE_CHECKING, List, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query import QuerySet
from modeltranslation.manager import MultilingualManager

from users.models import User

if TYPE_CHECKING:
    from professionals.models import Professional


class ProfessionalLocationManager(models.Manager):
    """The professional location manager."""

    def get_list(self) -> QuerySet:
        """Return a list of professional locations."""
        return self.all().select_related(
            "country",
            "region",
            "subregion",
            "city",
            "district",
            "postal_code",
            "professional",
            "professional__user",
            "created_by",
            "modified_by",
        )

    def get_user_list(self, user: User) -> QuerySet:
        """Return a list of professional localizations filtered by user."""
        return self.get_list().filter(professional__user=user)


class ProfessionalPhotoManager(models.Manager):
    """The professional photo manager."""

    def get_list(self) -> QuerySet:
        """Return a list of professional photos."""
        return self.all().select_related(
            "professional",
            "created_by",
            "modified_by",
            "professional__user",
        )


class ProfessionalEducationManager(models.Manager):
    """The professional education manager."""

    def get_list(self) -> QuerySet:
        """Return a list of professional educations."""
        return self.all().select_related(
            "professional",
            "created_by",
            "modified_by",
            "professional__user",
        )


class ProfessionalCertificateManager(models.Manager):
    """The professional certificate manager."""

    def get_list(self) -> QuerySet:
        """Return a list of professional certificates."""
        return self.all().select_related(
            "professional",
            "created_by",
            "modified_by",
            "professional__user",
        )


class ProfessionalExperienceManager(models.Manager):
    """The professional education manager."""

    def get_list(self) -> QuerySet:
        """Return a list of professional educations."""
        return self.all().select_related(
            "professional",
            "created_by",
            "modified_by",
            "professional__user",
        )


class ProfessionalContactManager(models.Manager):
    """The professional contact manager."""

    def get_list(self) -> QuerySet:
        """Return a list of professional contacts."""
        return self.all().select_related(
            "professional",
            "contact",
            "created_by",
            "modified_by",
            "professional__user",
        )


class ProfessionalTagManager(models.Manager):
    """The professional tag manager."""

    def get_list(self) -> QuerySet:
        """Return a list of professional tags."""
        return self.all().select_related("created_by", "modified_by",
                                         "professional")

    def get_names(self) -> QuerySet:
        """Return a list of professional tags names."""
        return self.all().distinct("name").order_by("name").values("name")


class ProfessionalManager(models.Manager):
    """The professional manager."""

    def get_by_params(self, **kwargs) -> Optional["Professional"]:
        """Return a professional by a pk."""
        try:
            return self.select_related(
                "created_by",
                "modified_by",
                "user",
                "subcategory",
                "subcategory__category",
            ).get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def get_list(self) -> QuerySet:
        """Return a list of professionals."""
        return self.all().select_related(
            "created_by",
            "modified_by",
            "user",
            "user__settings",
            "subcategory",
            "subcategory__category",
        )

    def get_extended_list(self) -> QuerySet:
        """Return a list of professionals."""
        return self.get_list().prefetch_related(
            "user__languages",
            "tags",
            "contacts",
            "locations",
            "experience_entries",
            "educations",
            "certificates",
        )

    def get_for_avaliability_generation(
        self,
        ids: Optional[List[int]] = None,
    ) -> QuerySet:
        """Return a list of professionals for availability generation."""
        query = self.get_list()
        if not ids:
            return query
        return query.filter(pk__in=ids)

    def get_user_list(self, user: User) -> QuerySet:
        """Return a list of professionals filtered by user."""
        return self.get_list().filter(user=user)


class CategoryManager(MultilingualManager):
    """The category manager."""

    def get_list(self) -> QuerySet:
        """Return a list of contacts."""
        return self.all().select_related("created_by", "modified_by")


class SubcategoryManager(MultilingualManager):
    """The subcategory manager."""

    def get_list(self) -> QuerySet:
        """Return a list of contacts."""
        return self.all().select_related(
            "created_by",
            "modified_by",
            "category",
        )
