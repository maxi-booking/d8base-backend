"""The professionals managers module."""
from django.db import models
from django.db.models.query import QuerySet
from modeltranslation.manager import MultilingualManager

from users.models import User


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

    def get_list(self) -> QuerySet:
        """Return a list of professionals."""
        return self.all().select_related(
            "created_by",
            "modified_by",
            "user",
            "subcategory",
            "subcategory__category",
        )

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
