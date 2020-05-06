"""The professionals models module."""

from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from contacts.models import ContactMixin
from d8b.models import CommonInfo
from location.models import LocationMixin
from location.services import LocationAutofiller
from users.models import User

from .managers import (CategoryManager, ProfessionalContactManager,
                       ProfessionalLocationManager, ProfessionalManager,
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

    # reviews and rating
    # services
    # work experience *
    # education *
    # certifications *
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


class ProfessionalContact(CommonInfo, ContactMixin):
    """The professional contact class."""

    objects = ProfessionalContactManager()

    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name=_('professional'),
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.professional}: {self.contact} {self.value}'

    class Meta(CommonInfo.Meta):
        """The professional contact class META class."""

        abstract = False
        unique_together = (('value', 'professional', 'contact'), )


class ProfessionalLocation(CommonInfo, LocationMixin):
    """The user location class."""

    objects = ProfessionalLocationManager()
    autofiller = LocationAutofiller

    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='locations',
        verbose_name=_('professional'),
    )
    is_default = models.BooleanField(
        default=False,
        help_text=_('is default location?'),
        verbose_name=_('is default'),
    )

    def save(self, **kwargs):
        """Save the object."""
        self.autofiller(self).autofill_location()
        super().save(**kwargs)

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.professional}: ' + ', '.join(
            map(str, filter(None, [self.country, self.city, self.address])))

    class Meta(CommonInfo.Meta):
        """The user location class META class."""

        abstract = False
