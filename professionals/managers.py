"""The professionals managers module."""
from django.db.models.query import QuerySet
from modeltranslation.manager import MultilingualManager


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
