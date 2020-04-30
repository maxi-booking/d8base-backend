"""The professionals models module."""

from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from d8b.models import CommonInfo
from users.models import User

from .managers import (CategoryManager, ProfessionalManager,
                       ProfessionalTagManager, SubcategoryManager)


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


class Professional(CommonInfo):
    """The professional profile class."""

    # favorite master --
    # reviews and rating
    # servicesMaking Anagrams
    # location --
    # work experience
    # education
    # certifications
    # contacts --
    # portfolio/photos
    # payments

    objects = ProfessionalManager()

    LEVEL_JUNIOR: str = 'junior'
    LEVEL_MIDDLE: str = 'middle'
    LEVEL_SENIOR: str = 'senior'
    LEVEL_CHOICES = [
        (LEVEL_JUNIOR, _('junior')),
        (LEVEL_MIDDLE, _('middle')),
        (LEVEL_SENIOR, _('senior')),
    ]

    name = models.CharField(
        _('name'),
        max_length=255,
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True,
    )
    company = models.CharField(
        _('company'),
        max_length=255,
        null=True,
        blank=True,
    )
    experience = models.PositiveSmallIntegerField(
        _('years of experience'),
        null=True,
        blank=True,
    )
    level = models.CharField(
        _('level'),
        max_length=20,
        choices=LEVEL_CHOICES,
        null=True,
        blank=True,
    )
    is_auto_order_confirmation = models.BooleanField(
        default=True,
        help_text=_('are orders confirmed automatically?'),
        verbose_name=_('is auto order confirmation?'),
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        related_name='professionals',
        verbose_name=_('subcategory'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='professionals',
        verbose_name=_('user'),
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.user}: {self.name}'


class BaseTag(CommonInfo):
    """The base tag class."""

    name = models.CharField(
        _('name'),
        max_length=255,
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.name}'

    class Meta(CommonInfo.Meta):
        """The contact class META class."""

        abstract = True


class ProfessionalTag(BaseTag):
    """The base tag class."""

    objects = ProfessionalTagManager()

    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name=_('professional'),
    )

    class Meta(BaseTag.Meta):
        """The contact class META class."""

        abstract = False
        unique_together = (('name', 'professional'), )
