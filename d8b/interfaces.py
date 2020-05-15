"""The d8b interfaces module."""
import datetime
from typing import Optional

from django.db import models


class AbstractDefaultEntry():
    """The absctract class with default field."""

    is_default: bool
    objects: models.Manager


class StartEndDateEntry():
    """The absctract class with start and end dates."""

    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    is_still_here: bool
