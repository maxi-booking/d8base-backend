"""The logging tests module."""
from d8b.settings import get_settings


def test_get_settings():
    """Should log the function."""
    assert get_settings("LANGUAGE_CODE") == "en"
    assert get_settings("UNITS_IMPERIAL") == 1
    assert get_settings("INVALID") is None
