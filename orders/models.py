"""The orders models module."""
from typing import Type

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from phonenumber_field.modelfields import PhoneNumberField

from d8b.models import CommonInfo, ValidationMixin
from schedule.models import AbstractPeriod

from .managers import OrdersManager
from .services import OrderAutoFiller
from .validators import (validate_order_availability, validate_order_client,
                         validate_order_client_location, validate_order_dates,
                         validate_order_service_location,
                         validate_order_status)


class Order(AbstractPeriod, CommonInfo, ValidationMixin):
    """The order class."""

    filler: Type = OrderAutoFiller

    validators = [
        validate_order_dates,
        validate_order_status,
        validate_order_client,
        validate_order_client_location,
        validate_order_service_location,
        validate_order_availability,
    ]

    objects: OrdersManager = OrdersManager()

    STATUS_NOT_CONFIRMED: str = "not_confirmed"
    STATUS_CONFIRMED: str = "confirmed"
    STATUS_PAID: str = "paid"
    STATUS_COMPLETED: str = "completed"
    STATUS_CANCELED: str = "canceled"
    STATUS_CHOICES = [
        (STATUS_NOT_CONFIRMED, _("not confirmed")),
        (STATUS_CONFIRMED, _("confirmed")),
        (STATUS_PAID, _("paid")),
        (STATUS_COMPLETED, _("completed")),
        (STATUS_CANCELED, _("canceled")),
    ]

    service = models.ForeignKey(
        "services.Service",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("service"),
    )
    service_location = models.ForeignKey(
        "services.ServiceLocation",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("service location"),
        null=True,
        blank=True,
    )
    client_location = models.ForeignKey(
        "users.UserLocation",
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name=_("client location"),
        null=True,
        blank=True,
    )
    client = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("user"),
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_CONFIRMED,
    )
    note = models.CharField(
        _("note"),
        null=True,
        blank=True,
        max_length=255,
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
    remind_before = models.PositiveIntegerField(
        _("remind"),
        null=True,
        blank=True,
        help_text=_("number of minutes for a reminder before the event"),
        db_index=True,
    )
    is_another_person = models.BooleanField(
        default=False,
        verbose_name=_("Order for another person?"),
        db_index=True,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=30,
        null=False,
        blank=True,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        null=False,
        blank=True,
    )
    phone = PhoneNumberField(
        _("phone"),
        blank=True,
        null=True,
        db_index=True,
    )

    def full_clean(self, exclude=None, validate_unique=True):
        """Validate the object."""
        self.filler(self).fill()
        return super().full_clean(exclude, validate_unique)

    def clean(self):
        """Validate the object."""
        self.filler(self).fill()
        return super().clean()

    def save(self, **kwargs):
        """Save the object."""
        self.filler(self).fill()
        super().save(**kwargs)

    @property
    def duration(self) -> float:
        """Return the order duration."""
        delta = self.end_datetime - self.start_datetime
        return delta.total_seconds() / 60

    def __str__(self) -> str:
        """Return the string representation."""
        return f"#{self.pk}: {super().__str__()}"

    class Meta(CommonInfo.Meta):
        """The metainformation."""

        abstract = False
