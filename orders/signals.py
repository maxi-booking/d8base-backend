"""The orders signals module."""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from schedule.availability import generate_for_order

from .models import Order


@receiver(
    post_save,
    sender=Order,
    dispatch_uid="order_post_save",
)
@receiver(
    post_delete,
    sender=Order,
    dispatch_uid="order_post_delete",
)
def professional_schedule_receiver(
    sender,
    instance: Order,
    **kwargs,
):
    """Generate the schedule."""
    # pylint: disable=unused-argument
    generate_for_order(instance)
