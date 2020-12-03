"""The location documents module."""
from cities.models import AlternativeName, City
from django.db.models.query import QuerySet
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class CityDocument(Document):
    """The service elasticsearch document."""

    alt_names = fields.TextField(fields={"raw": fields.KeywordField()}, )

    def prepare_alt_names(self, instance: City) -> str:
        """Return the alt names as a string."""
        # pylint: disable=no-self-use
        return " ".join([t.name for t in instance.alt_names.all()])

    class Index:
        """The index settings class."""

        name = "cities"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        """The django settings class."""

        model = City
        related_models = [AlternativeName]
        fields = ["name", "name_std"]

    def get_queryset(self) -> QuerySet:
        """Return the queryset."""
        return super().get_queryset().prefetch_related("alt_names")

    def get_instances_from_related(
        self,
        related_instance: AlternativeName,
    ) -> QuerySet:
        """Get a service from the tag."""
        # pylint: disable=no-self-use
        return related_instance.city_set.all()
