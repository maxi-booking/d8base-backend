"""The d8b enum module."""
from enum import Enum as Base
from typing import Any, Tuple


class Enum(Base):
    """The enum class."""

    @classmethod
    def values(cls) -> Tuple[Any, ...]:
        """Return a list of values."""
        return tuple([v.value for v in cls])
