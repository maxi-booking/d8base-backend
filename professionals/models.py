"""The professionals models module."""

from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from contacts.models import ContactMixin
from d8b.models import CommonInfo, ValidationMixin
from d8b.validators import validate_date_in_past, validate_start_end_dates
from location.models import LocationMixin
from location.services import LocationAutofiller
from users.models import User, UserLocation

from .managers import (CategoryManager, ProfessionalContactManager,
                       ProfessionalEducationManager,
                       ProfessionalLocationManager, ProfessionalManager,
                       ProfessionalTagManager, SubcategoryManager)
from .services import LocationCopyAutofiller
from .validators import validate_user_location


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

    name = models.CharField(_('name'), max_length=255)

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


class ProfessionalEducation(CommonInfo, ValidationMixin):
    """The professional education class."""

    objects = ProfessionalEducationManager()
    validators = [validate_start_end_dates]

    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='educations',
        verbose_name=_('professional'),
    )
    university = models.CharField(
        _('university'),
        max_length=255,
        help_text=_('school/university'),
    )
    deegree = models.CharField(
        _('deegree'),
        max_length=255,
        null=True,
        blank=True,
    )
    field_of_study = models.CharField(
        _('field_of_study'),
        max_length=255,
        null=True,
        blank=True,
    )
    is_still_here = models.BooleanField(
        _('is_still_here'),
        default=False,
        help_text=_('Is the professional still learning here?'),
    )
    start_date = models.DateField(
        _('start date'),
        blank=True,
        null=True,
        validators=[validate_date_in_past],
    )
    end_date = models.DateField(
        _('end date'),
        blank=True,
        null=True,
        validators=[validate_date_in_past],
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.professional}: {self.university}'

    class Meta(CommonInfo.Meta):
        """The Metainformation."""

        abstract = False


class ProfessionalLocation(CommonInfo, LocationMixin, ValidationMixin):
    """The professional location class."""

    objects = ProfessionalLocationManager()
    autofiller = LocationAutofiller
    copy_autofiller = LocationCopyAutofiller
    validators = [validate_user_location]

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
    user_location = models.ForeignKey(
        UserLocation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='professional_locations',
        verbose_name=_('user location'),
        help_text=_('user location to copy the location'),
    )

    def save(self, **kwargs):
        """Save the object."""
        self.copy_autofiller(self, self.user_location).autofill_location()
        self.autofiller(self).autofill_location()
        super().save(**kwargs)

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.professional}: ' + ', '.join(
            map(str, filter(None, [self.country, self.city, self.address])))

    class Meta(CommonInfo.Meta):
        """The user location class META class."""

        abstract = False
