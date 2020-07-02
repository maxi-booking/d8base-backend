"""The views tests module."""
import pytest
from django.db.models import Q
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse
from push_notifications.models import GCMDevice

from communication.models import Message
from conftest import OBJECTS_TO_CREATE
from users.models import User

pytestmark = pytest.mark.django_db


def test_received_messages_list(
    user: User,
    client_with_token: Client,
    messages: QuerySet,
):
    """Should return a list of received messages."""
    obj = messages.filter(recipient=user).first()
    response = client_with_token.get(reverse('messages-received-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['results'][0]['sender'] == obj.sender.pk
    assert data['results'][0]['subject'] == obj.subject


def test_received_message_detail(
    user: User,
    client_with_token: Client,
    messages: QuerySet,
):
    """Should return a received message."""
    obj = messages.filter(recipient=user).first()
    assert not obj.is_read
    response = client_with_token.get(
        reverse('messages-received-detail', args=[obj.pk]))
    data = response.json()
    obj.refresh_from_db()
    assert response.status_code == 200
    assert data['body'] == obj.body
    assert obj.is_read


def test_received_message_delete(
    user: User,
    client_with_token: Client,
    messages: QuerySet,
):
    """Should delete a received message."""
    obj = messages.filter(recipient=user).first()

    assert not obj.is_deleted_from_recipient
    assert not obj.is_read

    response = client_with_token.delete(
        reverse('messages-received-detail', args=[obj.pk]))
    obj.refresh_from_db()
    assert response.status_code == 204
    assert obj.is_read
    assert obj.is_deleted_from_recipient
    assert obj.delete_from_recipient_datetime
    assert not obj.is_deleted_from_sender


def test_sent_messages_list(
    user: User,
    client_with_token: Client,
    messages: QuerySet,
):
    """Should return a list of sent messages."""
    obj = messages.filter(sender=user).first()
    response = client_with_token.get(reverse('messages-sent-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['results'][0]['recipient'] == obj.recipient.pk
    assert data['results'][0]['subject'] == obj.subject


def test_sent_message_detail(
    user: User,
    client_with_token: Client,
    messages: QuerySet,
):
    """Should return a sent message."""
    obj = messages.filter(sender=user).first()
    response = client_with_token.get(
        reverse('messages-sent-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['body'] == obj.body


def test_sent_message_create(
    admin: User,
    client_with_token: Client,
):
    """Should return a sent message."""
    response = client_with_token.post(
        reverse('messages-sent-list'),
        {
            'recipient': admin.pk,
            'subject': 'test subject',
            'body': 'test body',
        },
    )
    data = response.json()
    assert response.status_code == 201
    assert data['subject'] == 'test subject'


def test_sent_message_update(
    user: User,
    client_with_token: Client,
    messages: QuerySet,
):
    """Should update a sent message."""
    obj = messages.filter(sender=user).first()
    response = client_with_token.patch(
        reverse('messages-sent-detail', args=[obj.pk]),
        {
            'body': 'new body',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.body == 'new body'
    assert obj.modified_by == user


def test_sent_read_message_update(
    user: User,
    client_with_token: Client,
    messages: QuerySet,
):
    """Should not update a sent read message."""
    obj = messages.filter(sender=user).first()
    obj.is_read = True
    obj.save()
    response = client_with_token.patch(
        reverse('messages-sent-detail', args=[obj.pk]),
        {
            'body': 'new body',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 400


def test_sent_message_delete(
    user: User,
    client_with_token: Client,
    messages: QuerySet,
):
    """Should mark as deleted a sent read message."""
    obj = messages.filter(sender=user).first()
    obj.is_read = True
    obj.save()

    assert not obj.is_deleted_from_sender

    response = client_with_token.delete(
        reverse('messages-sent-detail', args=[obj.pk]))
    obj.refresh_from_db()
    assert response.status_code == 204
    assert obj.is_deleted_from_sender
    assert obj.delete_from_sender_datetime
    assert not obj.is_deleted_from_recipient


def test_sent_unread_message_delete(
    user: User,
    client_with_token: Client,
    messages: QuerySet,
):
    """Should be able to delete a unread sent message."""
    obj = messages.filter(sender=user).first()
    response = client_with_token.delete(
        reverse('messages-sent-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert messages.filter(pk=obj.pk).count() == 0


def test_device_fcm_create(
    user: User,
    client_with_token: Client,
):
    """Should create a fcm device."""
    response = client_with_token.post(
        reverse('communication-devices-fmc-list'),
        {
            'registration_id': 'test id',
            'name': 'test device',
            'cloud_message_type': 'FCM',
        },
    )
    data = response.json()
    device = GCMDevice.objects.first()
    assert response.status_code == 201
    assert data['name'] == 'test device'
    assert device.user == user
    assert device.registration_id == 'test id'


def test_user_reviews_list(
    user: User,
    client_with_token: Client,
    reviews: QuerySet,
):
    """Should return a user reviews list."""
    obj = reviews.filter(user=user).first()
    response = client_with_token.get(reverse('user-reviews-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 1
    assert data['results'][0]['title'] == obj.title


def test_user_review_detail(
    user: User,
    client_with_token: Client,
    reviews: QuerySet,
):
    """Should return a user review."""
    obj = reviews.filter(user=user).first()
    response = client_with_token.get(
        reverse('user-reviews-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['description'] == obj.description


def test_user_review_restricted_entry(
    admin: User,
    client_with_token: Client,
    reviews: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = reviews.filter(user=admin).first()
    response = client_with_token.patch(
        reverse('user-reviews-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_review_create(
    user: User,
    admin: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user review object."""
    professional = professionals.filter(user=admin).first()
    response = client_with_token.post(
        reverse('user-reviews-list'),
        {
            'title': 'test title',
            'description': 'test description',
            'rating': 4,
            'professional': professional.pk,
            'user': user,
        },
    )
    review = user.reviews.first()
    assert response.status_code == 201
    assert review.title == 'test title'


def test_user_review_update(
    user: User,
    client_with_token: Client,
    reviews: QuerySet,
):
    """Should be able to update a user review."""
    obj = reviews.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-reviews-detail', args=[obj.pk]),
        {
            'title': 'new title',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.title == 'new title'
    assert obj.user == user
    assert obj.modified_by == user


def test_user_review_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    reviews: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = reviews.filter(user=admin).first()
    response = client_with_token.post(
        reverse('user-reviews-detail', args=[obj.pk]), {'name': 'x'})
    assert response.status_code == 405


def test_user_review_delete(
    user: User,
    client_with_token: Client,
    reviews: QuerySet,
):
    """Should be able to delete a user review."""
    obj = reviews.filter(user=user).first()
    response = client_with_token.delete(
        reverse('user-reviews-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert reviews.filter(pk=obj.pk).count() == 0


def test_user_review_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    reviews: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = reviews.filter(user=admin).first()
    response = client_with_token.delete(
        reverse('user-reviews-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_review_comments_list(
    user: User,
    client_with_token: Client,
    review_comments: QuerySet,
):
    """Should return a user review comments list."""
    obj = review_comments.filter(user=user).first()
    response = client_with_token.get(reverse('user-review-comments-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 1
    assert data['results'][0]['title'] == obj.title


def test_user_review_comment_detail(
    user: User,
    client_with_token: Client,
    review_comments: QuerySet,
):
    """Should return a user review comment."""
    obj = review_comments.filter(user=user).first()
    response = client_with_token.get(
        reverse('user-review-comments-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['description'] == obj.description


def test_user_review_comment_restricted_entry(
    admin: User,
    client_with_token: Client,
    review_comments: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = review_comments.filter(user=admin).first()
    response = client_with_token.patch(
        reverse('user-review-comments-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_review_comment_create(
    user: User,
    client_with_token: Client,
    reviews: QuerySet,
):
    """Should be able to create a user review comment object."""
    review = reviews.filter(professional__user=user).first()
    response = client_with_token.post(
        reverse('user-review-comments-list'),
        {
            'title': 'test title',
            'description': 'test description',
            'review': review.pk,
            'user': user,
        },
    )
    review = user.review_comments.first()
    assert response.status_code == 201
    assert review.title == 'test title'


def test_user_review_comment_update(
    user: User,
    client_with_token: Client,
    review_comments: QuerySet,
):
    """Should be able to update a user review comment."""
    obj = review_comments.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-review-comments-detail', args=[obj.pk]),
        {
            'title': 'new title',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.title == 'new title'
    assert obj.user == user
    assert obj.modified_by == user


def test_user_review_comment_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    review_comments: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = review_comments.filter(user=admin).first()
    response = client_with_token.post(
        reverse('user-review-comments-detail', args=[obj.pk]), {'name': 'x'})
    assert response.status_code == 405


def test_user_review_comment_delete(
    user: User,
    client_with_token: Client,
    review_comments: QuerySet,
):
    """Should be able to delete a user review."""
    obj = review_comments.filter(user=user).first()
    response = client_with_token.delete(
        reverse('user-review-comments-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert review_comments.filter(pk=obj.pk).count() == 0


def test_user_review_comment_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    review_comments: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = review_comments.filter(user=admin).first()
    response = client_with_token.delete(
        reverse('user-review-comments-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_messages_list(
        admin: User,
        user: User,
        client_with_token: Client,
        messages: QuerySet,  # pylint: disable=unused-argument
):
    """Should return a  messages list."""

    def request(interlocutor=None):
        """Make request."""
        url = reverse('messages-list-list')
        if interlocutor:
            url += f'?interlocutor={interlocutor.pk}'
        response = client_with_token.get(url)
        data = response.json()
        assert response.status_code == 200
        return data

    data = request()
    assert data['count'] == OBJECTS_TO_CREATE * 2

    Message.objects.create(
        sender=admin,
        recipient=user,
        body='admin->user',
    )
    data = request()
    assert data['count'] == OBJECTS_TO_CREATE * 2 + 1
    assert data['results'][0]['body'] == 'admin->user'

    Message.objects.filter(
        sender=user,
        recipient=admin,
    ).update(is_deleted_from_sender=True)

    data = request()
    assert data['count'] == OBJECTS_TO_CREATE + 1

    assert Message.objects.filter(
        sender=admin,
        recipient=user,
        is_read=True,
    ).count() == 0
    data = request(admin)
    assert Message.objects.filter(
        sender=admin,
        recipient=user,
        is_read=False,
    ).count() == 0


def test_latest_distinct_messages_list(
    admin: User,
    user: User,
    users: QuerySet,
    client_with_token: Client,
    messages: QuerySet,
):
    """Should return a latest distinct messages list."""

    def request() -> list:
        """Make request."""
        response = client_with_token.get(reverse('messages-latest-list'))
        data = response.json()
        assert response.status_code == 200
        return data

    obj = messages.filter(Q(recipient=user) | Q(sender=user)).\
        order_by('-created').first()
    user_another = users.first()

    data = request()
    assert len(data) == 1
    assert data[0]['subject'] == obj.subject
    assert data[0]['sender']['email'] == obj.sender.email

    Message.objects.create(
        sender=admin,
        recipient=user,
        body='admin->user',
    )
    data = request()
    assert len(data) == 1
    assert data[0]['body'] == 'admin->user'
    assert data[0]['sender']['email'] == admin.email

    Message.objects.create(
        sender=user,
        recipient=admin,
        body='user->admin',
    )
    data = request()
    assert len(data) == 1
    assert data[0]['body'] == 'user->admin'
    assert data[0]['sender']['email'] == user.email

    # Send message to the another user from admin
    Message.objects.create(
        sender=admin,
        recipient=user_another,
        body='admin->another',
    )
    data = request()
    assert len(data) == 1
    assert data[0]['body'] == 'user->admin'
    assert data[0]['sender']['email'] == user.email

    # Send message to the another user from the user
    Message.objects.create(
        sender=user,
        recipient=user_another,
        body='user->another',
    )
    data = request()
    assert len(data) == 2
    assert data[0]['body'] == 'user->another'
    assert data[0]['sender']['email'] == user.email
    assert data[0]['recipient']['email'] == user_another.email

    # Delete message to the another user from the user
    Message.objects.filter(
        sender=user,
        recipient=user_another,
    ).update(is_deleted_from_sender=True)
    data = request()
    assert len(data) == 1

    # Send message to the user from the another user
    Message.objects.create(
        sender=user_another,
        recipient=user,
        body='another->user',
    )
    data = request()
    assert len(data) == 2
    assert data[0]['body'] == 'another->user'
    assert data[0]['sender']['email'] == user_another.email
    assert data[0]['recipient']['email'] == user.email

    # Delete message to the user from the another user
    Message.objects.filter(
        sender=user_another,
        recipient=user,
    ).update(is_deleted_from_recipient=True)
    data = request()
    assert len(data) == 1
