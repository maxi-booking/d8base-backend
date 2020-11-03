"""The generate slots command."""

from typing import Optional

import arrow
from django.core.management.base import BaseCommand
from tqdm import tqdm

from professionals.models import Professional
from schedule.availability import (generate_for_professional,
                                   generate_for_service)
from services.models import Service


class Command(BaseCommand):
    """The generate slot command."""

    help = "Generate professional availability slots."

    start: Optional[arrow.Arrow]
    end: Optional[arrow.Arrow]

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

    def _generate_for_professional(self, professional: Professional) -> None:
        """Generate for the professional."""
        generate_for_professional(professional, start=self.start, end=self.end)

    def _generate_for_service(self, service: Service) -> None:
        """Generate for the service."""
        generate_for_service(service, start=self.start, end=self.end)

    def handle(self, *args, **options):
        """Run the command."""
        self.start = options["start"]
        self.end = options["end"]
        professionals = Professional.objects.\
            get_for_avaliability_generation(options["professionals"])
        services = Service.objects.\
            get_for_avaliability_generation(options["services"])
        total = professionals.count() + services.count()

        with tqdm(total=total) as progress:

            for professional in professionals.iterator():
                self._generate_for_professional(professional)
                progress.update(1)

            for service in services.iterator():
                self._generate_for_service(service)
                progress.update(1)

        self.stdout.write(self.style.SUCCESS("Slots have been generated."))
