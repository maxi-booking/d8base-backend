"""The signals tests module."""
from decimal import Decimal

import pytest
from django.db.models.query import QuerySet

from communication.models import Review
from users.models import User

pytestmark = pytest.mark.django_db


def test_review_post_save_and_delete(
    admin: User,
    professionals: QuerySet,
):
    """Should run the review post save and delete signals."""
    manager = Review.objects
    professional = professionals.first()
    manager.create(
        user=admin,
        professional=professional,
        description="description",
        rating=4,
    )
    professional.refresh_from_db()
    assert professional.rating == Decimal(4.00)
    manager.first().delete()

    professional.refresh_from_db()
    assert professional.rating is None
