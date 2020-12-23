"""The communication tasks module."""
from d8b.celery import app
from professionals.models import Professional
from services.models import Service

from .utils import (delete_expired_availability_slots,
                    generate_for_professional, generate_for_service)


@app.task
def remove_expired_availability_slots_task():
    """Delete the expired availability slots."""
    delete_expired_availability_slots()


@app.task(soft_time_limit=60 * 30)
def generate_future_availability_slots_task():
    """Generate future availability slots."""
    professionals = Professional.objects.get_for_avaliability_generation()
    services = Service.objects.get_for_avaliability_generation()

    for professional in professionals.iterator():
        generate_for_professional(professional=professional, append_days=True)

    for service in services.iterator():
        generate_for_service(service=service, append_days=True)
