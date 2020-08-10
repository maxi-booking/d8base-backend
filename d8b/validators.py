"""The professionals validators module."""
import datetime

import arrow
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .interfaces import StartEndDateEntry


def validate_start_end_dates(obj: StartEndDateEntry) -> None:
    """Check if the end date is greater than the start date."""
    if obj.start_date and obj.end_date and \
            obj.start_date >= obj.end_date:
        raise ValidationError(
            {"start_date": _("Start date is greater thant the end date.")})
    if obj.is_still_here and obj.end_date:
        raise ValidationError({
            "end_date":
                _("Either the_end date or is_still_here must be filled in.")
        })


def validate_date_in_past(date: datetime.date) -> None:
    """Make sure that the date is in the past."""
    if date > arrow.utcnow().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
    ).datetime:
        raise ValidationError(_("The date must be in the past."))


def validate_datetime_in_future(date: datetime.datetime) -> None:
    """Make sure that the date is in the future."""
    if date < arrow.utcnow().datetime:
        raise ValidationError(_("The datetime must be in the future."))
