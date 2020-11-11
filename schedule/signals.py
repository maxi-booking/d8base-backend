"""The signals module."""

from typing import Union

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from schedule.availability import (generate_for_professional,
                                   generate_for_service)
from services.models import Service

from .models import (ProfessionalClosedPeriod, ProfessionalSchedule,
                     ServiceClosedPeriod, ServiceSchedule)


@receiver(
    post_save,
    sender=ProfessionalSchedule,
    dispatch_uid="professional_schedule_post_save",
)
@receiver(
    post_delete,
    sender=ProfessionalSchedule,
    dispatch_uid="professional_schedule_post_delete",
)
@receiver(
    post_save,
    sender=ProfessionalClosedPeriod,
    dispatch_uid="professional_closed_period_post_save",
)
@receiver(
    post_delete,
    sender=ProfessionalClosedPeriod,
    dispatch_uid="professional_closed_period_post_delete",
)
def professional_schedule_receiver(
    sender,
    instance: Union[ProfessionalSchedule, ProfessionalClosedPeriod],
    **kwargs,
):
    """Generate the professional schedule."""
    # pylint: disable=unused-argument
    generate_for_professional(instance.professional)


@receiver(
    post_save,
    sender=ServiceSchedule,
    dispatch_uid="service_schedule_post_save",
)
@receiver(
    post_delete,
    sender=ServiceSchedule,
    dispatch_uid="service_schedule_post_delete",
)
@receiver(
    post_save,
    sender=ServiceClosedPeriod,
    dispatch_uid="service_closed_period_post_save",
)
@receiver(
    post_delete,
    sender=ServiceClosedPeriod,
    dispatch_uid="service_closed_period_post_delete",
)
def service_schedule_receiver(
    sender,
    instance: Union[ServiceSchedule, ServiceClosedPeriod],
    **kwargs,
):
    """Run the update availability tasks."""
    # pylint: disable=unused-argument
    generate_for_service(instance.service)


@receiver(
    post_save,
    sender=Service,
    dispatch_uid="service_post_save",
)
def service_receiver(
    sender,
    instance: Service,
    **kwargs,
):
    """Run the update availability tasks."""
    # pylint: disable=unused-argument
    if not instance.is_base_schedule:
        generate_for_service(instance)
