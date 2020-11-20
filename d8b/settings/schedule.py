"""Th schedule settings module."""
from datetime import time

from django.utils.translation import gettext_lazy as _

DAYS_MONDAY = 0
DAYS_TUESDAY = 1
DAYS_WEDNESDAY = 2
DAYS_THURSDAY = 3
DAYS_FRIDAY = 4
DAYS_SATURDAY = 5
DAYS_SUNDAY = 6

DAYS_OF_WEEK = (
    (DAYS_MONDAY, _("monday")),
    (DAYS_TUESDAY, _("tuesday")),
    (DAYS_WEDNESDAY, _("wednesday")),
    (DAYS_THURSDAY, _("thursday")),
    (DAYS_FRIDAY, _("friday")),
    (DAYS_SATURDAY, _("saturday")),
    (DAYS_SUNDAY, _("sunday")),
)

SCHEDULE_START_TIME = time(9, 00)
SCHEDULE_END_TIME = time(18, 00)
SCHEDULE_MINIMAL_TIME_SPAN = 15

AVAILABILITY_DAYS_TO_APPEND = 3
AVAILABILITY_MIN_SLOT_DIFF_TO_COMBINE = 70

D8B_BOOKING_INTERVAL = 15
D8B_REMINDER_INTERVAL = 5
