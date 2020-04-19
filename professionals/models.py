"""The professionals models module."""

from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from d8b.models import CommonInfo

from .managers import CategoryManager, SubcategoryManager

# from users.models import User


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


# class Professional(CommonInfo):
#     """The professional profile class."""

#     # company
#     # experience years
#     # level
#     # instant confirmation

#     # favorite master
#     # reviews and rating
#     # services
#     # location
#     # work experience
#     # education
#     # certifications
#     # contacts
#     # tags
#     # portfolio/photos
#     # payments

#     name = models.CharField(
#         _('name'),
#         max_length=255,
#     )
#     description = models.TextField(
#         _('description'),
#         null=True,
#         blank=True,
#     )
#     subcategory = models.ForeignKey(
#         Subcategory,
#         on_delete=models.PROTECT,
#         related_name='professionals',
#         verbose_name=_('user'),
#     )
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='professionals',
#         verbose_name=_('user'),
#     )
