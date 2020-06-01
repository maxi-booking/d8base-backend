"""The professionals admin module."""
from typing import Type

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from professionals.services import update_professional_rating

from .models import Review

# pylint: disable=unused-argument


# TODO: Test it
@receiver(
    post_save,
    sender=Review,
    dispatch_uid='communication_review_on_save',
)
def review_post_save(sender: Type, instance: Review, **kwargs):
    """Review post save signal."""
    update_professional_rating(instance.professional)


@receiver(
    post_delete,
    sender=Review,
    dispatch_uid='communication_review_on_save',
)
def review_post_delete(sender: Type, instance: Review, **kwargs):
    """Review post delete signal."""
    update_professional_rating(instance.professional)
