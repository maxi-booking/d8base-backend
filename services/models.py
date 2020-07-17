"""The services models module."""

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from d8b.models import CommonInfo, ValidationMixin
from d8b.services import RandomFilenameGenerator
from professionals.models import (BaseTag, PhotoMixin, Professional,
                                  ProfessionalLocation)

from .managers import (ServiceLocationManager, ServiceManager,
                       ServicePhotoManager, ServicePriceManager,
                       ServiceTagManager)
from .validators import validate_service_location, validate_service_price


class Service(CommonInfo):
    """The service class."""

    objects = ServiceManager()

    TYPE_ONLINE: str = "online"
    TYPE_PROFESSIONAL_LOCATION: str = "professional"
    TYPE_CLIENT_LOCATION: str = "client"
    TYPE_CHOICES = [
        (TYPE_ONLINE, _("online")),
        (TYPE_PROFESSIONAL_LOCATION, _("at the professional's location")),
        (TYPE_CLIENT_LOCATION, _("at the client's location")),
    ]

    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name=_("professional"),
    )
    name = models.CharField(
        _("name"),
        max_length=255,
        db_index=True,
    )
    description = models.TextField(
        _("description"),
        db_index=True,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(settings.D8B_SERVICE_DESCRIPTION_MIN_LENGTH)
        ],
    )
    duration = models.PositiveIntegerField(
        _("duration"),
        db_index=True,
        help_text=_("duration in minutes"),
    )
    service_type = models.CharField(
        _("account type"),
        max_length=20,
        choices=TYPE_CHOICES,
    )
    is_base_schedule = models.BooleanField(
        default=False,
        verbose_name=_("is the base schedule used?"),
        db_index=True,
    )
    is_auto_order_confirmation = models.BooleanField(
        default=True,
        help_text=_("are orders confirmed automatically?"),
        verbose_name=_("is auto order confirmation?"),
        db_index=True,
    )
    is_enabled = models.BooleanField(
        default=False,
        verbose_name=_("is enabled?"),
        db_index=True,
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.professional}: {self.name}"

    class Meta(CommonInfo.Meta):
        """The metainformation."""

        abstract = False


class ServiceTag(BaseTag):
    """The service tag class."""

    objects = ServiceTagManager()

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="tags",
        verbose_name=_("service"),
    )

    class Meta(BaseTag.Meta):
        """The metainformation."""

        abstract = False
        unique_together = (("name", "service"), )


class ServiceLocation(CommonInfo, ValidationMixin):
    """The service tag class."""

    objects = ServiceLocationManager()
    validators = [validate_service_location]

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="locations",
        verbose_name=_("service"),
    )
    location = models.ForeignKey(
        ProfessionalLocation,
        on_delete=models.CASCADE,
        related_name="service_locations",
        verbose_name=_("location"),
    )
    max_distance = models.DecimalField(
        _("maximum distance"),
        max_digits=7,
        decimal_places=1,
        db_index=True,
        null=True,
        blank=True,
        help_text=_("maximum travel distance from the location"),
        validators=[MinValueValidator(0.1)],
    )

    class Meta(CommonInfo.Meta):
        """The Metainformation."""

        abstract = False
        unique_together = (("location", "service"), )


class ServicePhoto(PhotoMixin):
    """The service photo class."""

    objects = ServicePhotoManager()

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name=_("service"),
    )
    photo = ProcessedImageField(
        upload_to=RandomFilenameGenerator("photos", "service"),
        processors=[
            ResizeToFit(
                width=settings.D8B_IMAGE_WIDTH,
                height=settings.D8B_IMAGE_HEIGHT,
                upscale=False,
            )
        ],
        format="PNG",
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.service}: {self.photo}"

    class Meta(PhotoMixin.Meta):
        """The Metainformation."""

        abstract = False


class Price(CommonInfo, ValidationMixin):
    """The service price class."""

    validators = [validate_service_price]
    objects = ServicePriceManager()

    TYPE_CASH: str = "cash"
    TYPE_ONLINE: str = "online"
    PAYMENT_METHODS_CHOICES = [
        (TYPE_CASH, _("cash")),
        (TYPE_ONLINE, _("online")),
    ]

    service = models.OneToOneField(
        Service,
        on_delete=models.CASCADE,
        related_name="price",
        verbose_name=_("service"),
    )
    price = MoneyField(
        max_digits=settings.D8B_MONEY_MAX_DIGITS,
        decimal_places=settings.D8B_MONEY_DECIMAL_PLACES,
        verbose_name=_("price"),
        null=True,
        blank=True,
        validators=[MinMoneyValidator(0)],
        db_index=True,
    )
    start_price = MoneyField(
        max_digits=settings.D8B_MONEY_MAX_DIGITS,
        decimal_places=settings.D8B_MONEY_DECIMAL_PLACES,
        verbose_name=_("start price"),
        null=True,
        blank=True,
        validators=[MinMoneyValidator(0)],
        db_index=True,
    )
    end_price = MoneyField(
        max_digits=settings.D8B_MONEY_MAX_DIGITS,
        decimal_places=settings.D8B_MONEY_DECIMAL_PLACES,
        verbose_name=_("end price"),
        null=True,
        blank=True,
        validators=[MinMoneyValidator(0)],
        db_index=True,
    )
    is_price_fixed = models.BooleanField(
        default=True,
        verbose_name=_("is the price fixed?"),
        db_index=True,
    )
    payment_methods = ArrayField(
        models.CharField(
            max_length=10,
            choices=PAYMENT_METHODS_CHOICES,
        ),
        verbose_name=_("payment methods"),
        db_index=True,
        help_text="available payment methods",
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return (f"{self.service}: {self.price}"
                f" ({self.start_price}-{self.end_price})")

    class Meta(CommonInfo.Meta):
        """The Metainformation."""

        abstract = False
