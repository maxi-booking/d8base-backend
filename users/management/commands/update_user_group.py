"""The update user group command."""
from django.core.management.base import BaseCommand

from users.repositories import GroupRepository


class Command(BaseCommand):
    """The update user group command class."""

    help = "Update the user group permissions"

    def handle(self, *args, **options):
        """Run the command."""
        group = GroupRepository().get_or_create_user_group(force_update=True)
        self.stdout.write(
            self.style.SUCCESS(f"The <{group}> group has been updated."))
