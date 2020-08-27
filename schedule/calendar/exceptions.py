"""The calendar exceptions module."""


class CalendarError(Exception):
    """The calendar base error."""


class CalendarValidationError(CalendarError):
    """The calendar validation error."""


class CalendarValueError(CalendarError):
    """The calendar value error."""
