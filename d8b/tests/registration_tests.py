"""The registration tests module."""
from d8b.registration import get_registration_urls


def test_get_registration_urls():
    """Should return the filtered registration URLs."""
    names = [u.name for u in get_registration_urls()]

    assert 'login' not in names
    assert 'logout' not in names
    assert 'verify-registration' not in names
    assert 'verify-email' not in names
    assert 'register-email' not in names
    assert 'register' in names
    assert len(names) == 5
