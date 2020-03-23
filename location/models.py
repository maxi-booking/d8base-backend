"""The location models module."""
from dataclasses import dataclass


@dataclass
class Language():
    """The language model class."""

    code: str
    name: str
