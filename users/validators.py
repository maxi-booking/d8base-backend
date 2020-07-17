"""The users validators module."""
from datetime import date

import arrow
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_birthday(birthday: date, min_age: int = 12) -> None:
    """Validate a birthday."""
    min_date = arrow.utcnow().shift(years=-min_age).date()
    if birthday > min_date:
        raise ValidationError(
            _("Minimal age is %(min_age)s years old."),
            params={"min_age": min_age},
        )
