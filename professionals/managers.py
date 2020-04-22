"""The professionals managers module."""
from django.db import models
from django.db.models.query import QuerySet
from modeltranslation.manager import MultilingualManager

from users.models import User


class ProfessionalTagManager(models.Manager):
    """The professional tag manager."""

    def get_list(self) -> QuerySet:
        """Return a list of professional tags."""
        return self.all().select_related('created_by', 'modified_by',
                                         'professional')

    def get_names(self) -> QuerySet:
        """Return a list of professional tags names."""
        return self.all().distinct('name').order_by('name').values('name')


class ProfessionalManager(models.Manager):
    """The professional manager."""

    def get_list(self) -> QuerySet:
        """Return a list of professionals."""
        return self.all().select_related('created_by', 'modified_by', 'user')

    def get_user_list(self, user: User) -> QuerySet:
        """Return a list of professionals filtered by user."""
        return self.get_list().filter(user=user)


class CategoryManager(MultilingualManager):
    """The category manager."""

    def get_list(self) -> QuerySet:
        """Return a list of contacts."""
        return self.all().select_related('created_by', 'modified_by')


class SubcategoryManager(MultilingualManager):
    """The subcategory manager."""

    def get_list(self) -> QuerySet:
        """Return a list of contacts."""
        return self.all().select_related(
            'created_by',
            'modified_by',
            'category',
        )
