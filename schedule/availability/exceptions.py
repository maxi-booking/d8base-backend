"""The availability exceptions module."""


class AvailabilityError(Exception):
    """The availability base error."""


class AvailabilityValueError(AvailabilityError):
    """The availability value error."""
