"""The routers tests module."""
from d8b.enum import Enum


def test_enum_values():
    """Should return a list of the enum values."""

    class Test(Enum):
        """Test enum."""

        ONE = "one"
        TWO = "two"

    assert Test.values() == ("one", "two")
