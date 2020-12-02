"""The professionals documents module."""

from django.db.models.query import QuerySet
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from search.elasticsearch import languages_analyzer

from .models import Professional, ProfessionalTag


@registry.register_document
class ProfessionalDocument(Document):
    """The professional elasticsearch document."""

    name = fields.TextField(
        analyzer=languages_analyzer,
        fields={"raw": fields.KeywordField()},
    )
    description = fields.TextField(
        analyzer=languages_analyzer,
        fields={"raw": fields.KeywordField()},
    )
    tags = fields.TextField(
        analyzer=languages_analyzer,
        fields={"raw": fields.KeywordField()},
    )

    def prepare_tags(self, instance: Professional) -> str:
        """Return the tags as a string."""
        # pylint: disable=no-self-use
        return " ".join([t.name for t in instance.tags.all()])

    class Index:
        """The index settings class."""

        name = "professionals"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        """The django settings class."""

        model = Professional
        fields = ["company"]
        related_models = [ProfessionalTag]

    def get_queryset(self) -> QuerySet:
        """Return the queryset."""
        return super().get_queryset().prefetch_related("tags")

    def get_instances_from_related(
        self,
        related_instance: ProfessionalTag,
    ) -> Professional:
        """Get a professional from the tag."""
        # pylint: disable=no-self-use
        return related_instance.professional
