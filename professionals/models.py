"""The professionals models module."""

from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from d8b.models import CommonInfo

from .managers import CategoryManager, SubcategoryManager


class BaseCategory(CommonInfo):
    """The base category class."""

    name = models.CharField(
        _('name'),
        max_length=255,
        blank=True,
        null=True,
    )
    description = models.CharField(
        _('description'),
        max_length=255,
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True,
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.name}'

    class Meta:
        """The contact class META class."""

        abstract = True
        ordering = ('order', )


class Category(BaseCategory, SortableMixin):
    """The professional category class."""

    objects = CategoryManager()

    class Meta(BaseCategory.Meta):
        """The contact class META class."""

        verbose_name_plural = _('categories')


class Subcategory(BaseCategory, SortableMixin):
    """The professional subcategory class."""

    objects = SubcategoryManager()

    category = SortableForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
    )

    class Meta(BaseCategory.Meta):
        """The contact class META class."""

        verbose_name_plural = _('subcategories')
