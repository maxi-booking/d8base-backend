"""The calendar response module."""
from typing import Optional

import arrow
import pytz

from services.models import Service


class CalendarResponse():
    """The calendar response."""

    service: Optional[Service] = None
    timezone: pytz.BaseTzInfo
    period_start: arrow.Arrow
    period_end: arrow.Arrow
    is_open: bool
    # owner: orders
