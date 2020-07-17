"""The services serializer fields module."""

from decimal import Decimal

from rest_framework import serializers

from d8b.units import convert_km_mi, convert_mi_km, is_imperial_units


class DistanceField(serializers.DecimalField):
    """The distance field."""

    def __init__(self, user, **kwargs):
        """Construct the object."""
        self.get_user = user
        super().__init__(**kwargs)

    def is_imperial_units(self) -> bool:
        """Check the request user units."""
        user = self.get_user(self)
        return is_imperial_units(user)

    def to_representation(self, value):
        """Return the representation of the value."""
        if self.is_imperial_units():
            value = convert_km_mi(value)
        return super().to_representation(value)

    def to_internal_value(self, data):
        """Return the internal value."""
        value = super().to_internal_value(data)
        if self.is_imperial_units():
            value = convert_mi_km(value)
        return value.quantize(Decimal(".0"))
