"""The orders serializers module."""
from django.conf import settings
from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

from d8b.serializers import ModelCleanFieldsSerializer
from services.models import Service, ServiceLocation
from users.models import UserLocation

from .models import Order


class SentOrderSerializer(ModelCleanFieldsSerializer):
    """The sent order serializer."""

    client = serializers.HiddenField(default=serializers.CurrentUserDefault())
    service = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Service.objects.get_list().filter(is_enabled=True),
    )
    service_location = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=ServiceLocation.objects.get_list(),
        allow_null=True,
        required=False,
    )
    client_location = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=UserLocation.objects.get_list(),
        allow_null=True,
        required=False,
    )
    price = serializers.HiddenField(default=None)
    price_amount = MoneyField(
        max_digits=settings.D8B_MONEY_MAX_DIGITS,
        decimal_places=settings.D8B_MONEY_DECIMAL_PLACES,
        read_only=True,
        source="price",
    )
    end_datetime = serializers.DateTimeField(allow_null=True, required=False)

    class Meta:
        """The metainformation."""

        model = Order

        fields = ("id", "service", "service_location", "client",
                  "client_location", "status", "note", "price", "price_amount",
                  "price_currency", "is_another_person", "first_name",
                  "last_name", "phone", "start_datetime", "end_datetime",
                  "created", "modified")
        read_only_fields = ("client", "status", "price", "price_currency",
                            "created", "modified", "created_by", "modified_by")
