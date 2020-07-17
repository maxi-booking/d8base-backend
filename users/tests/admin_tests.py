"""The users admin test module."""
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_admin_redirect(client):
    """Should return a redirect for non-authenticated users."""
    response = client.get(reverse("admin:users_user_changelist"))

    assert response.status_code == 302
    assert reverse("admin:login") in response["Location"]


def test_admin_list(admin, user, admin_client):
    """Should return the a list of users."""
    response = admin_client.get(reverse("admin:users_user_changelist"))

    assert response.status_code == 200
    assert admin.email.encode() in response.content
    assert user.email.encode() in response.content
