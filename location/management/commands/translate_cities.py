"""The translate cities command."""

from time import sleep
from typing import Tuple

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import activate
from tqdm import tqdm

from location import repositories as repo


class Command(BaseCommand):
    """The translate cities slot command."""

    help = "Translate the countries, regions, cities, and districts"

    DEFAULT_LANG: str = "en"

    lang: str
    sleep: float = 0
    repositories: Tuple[repo.BaseRepository, ...] = (
        repo.ContinentRepository(),
        repo.CountryRepository(),
        repo.RegionRepository(),
        repo.SubregionRepository(),
        repo.CityRepository(),
        repo.DistrictRepository(),
    )

    def add_arguments(self, parser):
        """Add arguments to the command."""
        parser.add_argument(
            "lang",
            type=str,
            choices=[
                i for i in settings.MODELTRANSLATION_LANGUAGES
                if i != self.DEFAULT_LANG
            ],
            help="The destination language",
        )
        parser.add_argument(
            "--sleep",
            type=float,
            default=self.sleep,
            help="The sleep interval in seconds between http request",
        )

    def handle(self, *args, **options):
        """Run the command."""
        self.lang = options["lang"]
        self.sleep = options["sleep"]
        activate(self.DEFAULT_LANG)

        for repository in self.repositories:
            objects = repository.get_to_translate(self.lang)
            self.stdout.write(self.style.NOTICE(objects.model.__name__))
            with tqdm(total=objects.count()) as progress:
                for obj in objects.iterator():
                    try:
                        repository.translate(obj, self.lang)
                    except Exception as error:  # pylint: disable=broad-except
                        self.stdout.write(self.style.ERROR(error))
                    progress.update(1)
                    sleep(self.sleep)

        self.stdout.write(self.style.SUCCESS("Objects have been translated."))
