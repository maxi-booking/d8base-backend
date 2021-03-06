"""The service serializers module."""
from typing import List

from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from djmoney.contrib.django_rest_framework import MoneyField
from djmoney.contrib.exchange.models import Rate
from drf_extra_fields.fields import Base64ImageField
from moneyed import CURRENCIES
from moneyed.localization import _FORMATTER
from rest_framework import serializers

from d8b.serializer_fields import DistanceField
from d8b.serializers import ModelCleanFieldsSerializer
from professionals.serializer_fields import AccountProfessionalForeignKey
from professionals.serializers import ProfessionalLocationInlineSerializer

from .models import Price, Service, ServiceLocation, ServicePhoto, ServiceTag
from .serializer_fields import (AccountProfessionalLocationForeignKey,
                                AccountServiceForeignKey)


class PriceSerializer(ModelCleanFieldsSerializer):
    """The price serializer."""

    service = AccountServiceForeignKey()
    price = MoneyField(
        max_digits=settings.D8B_MONEY_MAX_DIGITS,
        decimal_places=settings.D8B_MONEY_DECIMAL_PLACES,
        required=False,
        allow_null=True,
    )
    start_price = MoneyField(
        max_digits=settings.D8B_MONEY_MAX_DIGITS,
        decimal_places=settings.D8B_MONEY_DECIMAL_PLACES,
        required=False,
        allow_null=True,
    )
    end_price = MoneyField(
        max_digits=settings.D8B_MONEY_MAX_DIGITS,
        decimal_places=settings.D8B_MONEY_DECIMAL_PLACES,
        required=False,
        allow_null=True,
    )

    class Meta:
        """The metainformation."""

        model = Price
        fields = ("id", "service", "price", "price_currency", "start_price",
                  "start_price_currency", "end_price", "end_price_currency",
                  "is_price_fixed", "payment_methods", "modified",
                  "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")
        extra_kwargs = {"is_price_fixed": {"required": True}}


class ServiceTagSerializer(serializers.ModelSerializer):
    """The service tag serializer."""

    service = AccountServiceForeignKey()

    class Meta:
        """The metainformation."""

        model = ServiceTag
        fields = ("id", "service", "name", "created", "modified", "created_by",
                  "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ServiceTagListSerializer(serializers.ModelSerializer):
    """The service tag list serializer."""

    class Meta:
        """The metainformation."""

        model = ServiceTag
        fields = ("name", )


class ServiceSerializer(serializers.ModelSerializer):
    """The service serializer."""

    professional = AccountProfessionalForeignKey()
    price = PriceSerializer(many=False, read_only=True)

    class Meta:
        """The metainformation."""

        model = Service
        fields = ("id", "professional", "name", "description", "duration",
                  "booking_interval", "service_type", "is_base_schedule",
                  "is_auto_order_confirmation", "is_enabled", "price",
                  "created", "modified", "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ServiceLocationInlineSerializer(ModelCleanFieldsSerializer):
    """The service location inline serializer."""

    location = ProfessionalLocationInlineSerializer(
        many=False,
        read_only=True,
    )
    max_distance = DistanceField(
        max_digits=7,
        decimal_places=1,
        coerce_to_string=False,
        user=serializers.CurrentUserDefault(),
    )

    class Meta:
        """The metainformation."""

        model = ServiceLocation
        fields = ("id", "location", "max_distance", "created", "modified")
        read_only_fields = ("created", "modified")


class ServiceListSerializer(serializers.ModelSerializer):
    """The service list serializer."""

    price = PriceSerializer(many=False, read_only=True)
    tags = ServiceTagListSerializer(many=True, read_only=True)
    locations = ServiceLocationInlineSerializer(many=True, read_only=True)

    class Meta:
        """The metainformation."""

        model = Service
        fields = ("id", "professional", "name", "description", "duration",
                  "booking_interval", "service_type", "is_base_schedule",
                  "is_auto_order_confirmation", "is_enabled", "price", "tags",
                  "locations", "created", "modified")
        read_only_fields = ("created", "modified")


class ServiceLocationSerializer(ModelCleanFieldsSerializer):
    """The service location serializer."""

    service = AccountServiceForeignKey()
    location = AccountProfessionalLocationForeignKey(required=False)
    max_distance = DistanceField(
        max_digits=7,
        decimal_places=1,
        coerce_to_string=False,
        user=serializers.CurrentUserDefault(),
    )

    class Meta:
        """The metainformation."""

        model = ServiceLocation

        fields = ("id", "service", "location", "max_distance", "created",
                  "modified", "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class RateSerializer(serializers.ModelSerializer):
    """The rate model serializer."""

    title = serializers.SerializerMethodField()
    countries = serializers.SerializerMethodField()
    sign = serializers.SerializerMethodField()

    @staticmethod
    def get_sign(rate: Rate) -> str:
        """Get the currency sign."""
        result = _FORMATTER.get_sign_definition(rate.currency, get_language())

        return result[1].strip() or result[0].strip()

    @staticmethod
    def get_countries(rate: Rate) -> List[str]:
        """Get the currency countries."""
        currency = CURRENCIES.get(rate.currency)
        return getattr(currency, "countries", "-")

    @staticmethod
    def get_title(rate: Rate) -> str:
        """Get the currency title."""
        currency = CURRENCIES.get(rate.currency)
        return _(getattr(currency, "name", "-").strip())

    class Meta:
        """The metainformation."""

        model = Rate
        fields = ("currency", "title", "sign", "countries", "value")


class ServicePhotoSerializer(ModelCleanFieldsSerializer):
    """The service photo serializer."""

    service = AccountServiceForeignKey()

    photo_thumbnail = serializers.ImageField(read_only=True)
    photo = Base64ImageField(required=True)

    class Meta:
        """The metainformation."""

        model = ServicePhoto
        fields = ("id", "service", "name", "description", "order", "photo",
                  "photo_thumbnail", "created", "modified", "created_by",
                  "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ServicePhotoListSerializer(ModelCleanFieldsSerializer):
    """The service photo list serializer."""

    photo_thumbnail = serializers.ImageField(read_only=True)
    photo = Base64ImageField(required=False, read_only=True)

    class Meta:
        """The metainformation."""

        model = ServicePhoto
        fields = ("id", "service", "name", "description", "order", "photo",
                  "photo_thumbnail", "created", "modified")
        read_only_fields = ("created", "modified")
