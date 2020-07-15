"""The units tests module."""
from decimal import Decimal

import pytest
from django.utils import timezone

from d8b.serializer_fields import DistanceField
from users.models import User

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('value,expected', [
    (Decimal('1'), Decimal('0.6')),
    (Decimal('0.5'), Decimal('0.3')),
    (Decimal('22.5'), Decimal('14.0')),
])
def test_distance_field_to_representation(
    value: Decimal,
    expected: Decimal,
    user: User,
):
    """Should convert distance."""
    timezone.deactivate()
    field = DistanceField(
        max_digits=7,
        decimal_places=1,
        coerce_to_string=False,
        user=lambda x: user,
    )
    assert field.to_representation(value) == value
    assert field.to_internal_value(value) == value

    timezone.activate('America/New_York')
    assert field.to_representation(value) == expected
    assert field.to_internal_value(expected) == Decimal(value)
