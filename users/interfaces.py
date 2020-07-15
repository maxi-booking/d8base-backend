"""The users interfaces module."""

from dataclasses import dataclass


@dataclass
class UserCalculatedUnits():
    """The user calculated units."""

    is_imperial_units: bool
    timezone: str
    distance: str
