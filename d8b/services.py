"""The d8b services module."""

from .interfaces import AbstractDefaultEntry


class DefaultFieldSetter():
    """The default field autosetter."""

    entry: AbstractDefaultEntry

    def __init__(self, entry: AbstractDefaultEntry):
        """Construct the object."""
        self.entry = entry

    def process_default_for_query(self, **kwargs):
        """
        Set the is_default entry field.

        Set the is_default entry field value and update
        this field for the remain entries in the queryset.
        """
        is_default = self.entry.is_default
        query = self.entry.__class__.objects.filter(is_default=True, **kwargs)
        if not query.count():
            is_default = True
        self.entry.is_default = is_default
        if is_default:
            query.update(is_default=False)
