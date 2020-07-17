"""The urls tests module."""
from users.urls import get_urls


def test_get_registration_urls():
    """Should return the filtered registration URLs."""
    names = [u.name for u in get_urls()]

    assert "login" not in names
    assert "logout" not in names
    assert "register" in names
