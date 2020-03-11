"""The validators admin test module."""
import arrow
import pytest
from django.core.exceptions import ValidationError

from users.validators import validate_birthday


def test_validate_birthday():
    """The age should be less than the min_age."""
    with pytest.raises(ValidationError):
        validate_birthday(arrow.now().date())
    validate_birthday(arrow.now().shift(years=-15).date())
