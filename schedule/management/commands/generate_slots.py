"""The generate slots command."""

import arrow
from django.core.management.base import BaseCommand
from tqdm import tqdm

from professionals.models import Professional
from schedule.availability.generator import get_availability_generator
from schedule.availability.request import Request
from services.models import Service


class Command(BaseCommand):
    """The generate slot command."""

    help = "Generate professional availability slots."

    def add_arguments(self, parser):
        """Add arguments to the command."""
        parser.add_argument("--professionals", nargs="+", type=int)
        parser.add_argument("--services", nargs="+", type=int)
        parser.add_argument(
            "--start",
            type=arrow.get,
            help="YYYY-MM-DD",
        )
        parser.add_argument(
            "--end",
            type=arrow.get,
            help="YYYY-MM-DD",
        )

    def handle(self, *args, **options):
        """Run the command."""
        start = options["start"]
        end = options["end"]
        professionals = Professional.objects.\
            get_for_avaliability_generation(options["professionals"])
        services = Service.objects.\
            get_for_avaliability_generation(options["services"])
        total = professionals.count() + services.count()

        with tqdm(total=total) as progress:

            for professional in professionals.iterator():
                request = Request()
                request.professional = professional
                request.start_datetime = start
                request.end_datetime = end
                get_availability_generator(request).generate()
                progress.update(1)

            for service in services.iterator():
                request = Request()
                request.professional = service.professional
                request.service = service
                request.start_datetime = start
                request.end_datetime = end
                get_availability_generator(request).generate()
                progress.update(1)

        self.stdout.write(self.style.SUCCESS("Slots have been generated."))
