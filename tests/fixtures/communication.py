"""The communication fixtures module."""

import pytest
from django.db.models.query import QuerySet

from communication.models import (Message, Review, ReviewComment,
                                  SuggestedMessage)
from conftest import OBJECTS_TO_CREATE
from users.models import User

# pylint: disable=redefined-outer-name


@pytest.fixture
def suggested_messages(subcategories: QuerySet) -> QuerySet:
    """Return a subcategories queryset."""
    cat = subcategories.first()
    for i in range(0, OBJECTS_TO_CREATE):
        SuggestedMessage.objects.create(
            subcategory=cat,
            name_en=f"name {i}",
            body_en=f"description {i}",
            name_de=f"der name {i}",
            body_de=f"beschreibung {i}",
        )
    return SuggestedMessage.objects.get_list()


@pytest.fixture
def messages(admin: User, user: User, users: QuerySet) -> QuerySet:
    """Return a messages queryset."""
    user_one = users.first()
    user_two = users[1]

    for i in range(0, OBJECTS_TO_CREATE):
        Message.objects.create(
            sender=admin,
            recipient=user,
            subject=f"subject {i}",
            body=f"message body {i}",
        )
    for i in range(0, OBJECTS_TO_CREATE):
        Message.objects.create(
            sender=user,
            recipient=admin,
            subject=f"subject {i}",
            body=f"message body {i}",
        )
    for i in range(0, OBJECTS_TO_CREATE):
        Message.objects.create(
            sender=user_one,
            recipient=user_two,
            subject=f"subject user {i}",
            body=f"message body user {i}",
        )
    for i in range(0, OBJECTS_TO_CREATE):
        Message.objects.create(
            sender=user_two,
            recipient=user_one,
            subject=f"subject user {i}",
            body=f"message body user {i}",
        )
    return Message.objects.get_list()


@pytest.fixture
def reviews(admin: User, user: User, professionals: QuerySet) -> QuerySet:
    """Return a reviews queryset."""
    admin_professional = professionals.filter(user=admin).first()
    user_professional = professionals.filter(user=user).first()
    Review.objects.create(
        user=user,
        professional=admin_professional,
        title="title user",
        description="description user",
        rating=4,
    )
    Review.objects.create(
        user=admin,
        professional=user_professional,
        title="title admin",
        description="description admin",
        rating=5,
    )
    return Review.objects.get_list()


@pytest.fixture
def review_comments(admin: User, user: User, reviews: QuerySet) -> QuerySet:
    """Return a reviews queryset."""
    admin_review = reviews.filter(professional__user=admin).first()
    user_review = reviews.filter(professional__user=user).first()
    ReviewComment.objects.create(
        user=user,
        review=user_review,
        title="title user",
        description="description user",
    )
    ReviewComment.objects.create(
        user=admin,
        review=admin_review,
        title="title admin",
        description="description admin",
    )
    return ReviewComment.objects.get_list()
