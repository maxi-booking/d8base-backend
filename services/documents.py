"""The services documents module."""

from django.db.models.query import QuerySet
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from professionals.models import Professional, ProfessionalTag
from search.elasticsearch import languages_analyzer

from .models import Service, ServiceTag


@registry.register_document
class ServiceDocument(Document):
    """The service elasticsearch document."""

    name = fields.TextField(
        analyzer=languages_analyzer,
        fields={"raw": fields.KeywordField()},
    )
    professional_name = fields.TextField(
        analyzer=languages_analyzer,
        fields={"raw": fields.KeywordField()},
    )
    description = fields.TextField(
        analyzer=languages_analyzer,
        fields={"raw": fields.KeywordField()},
    )
    professional_description = fields.TextField(
        analyzer=languages_analyzer,
        fields={"raw": fields.KeywordField()},
    )
    tags = fields.TextField(
        analyzer=languages_analyzer,
        fields={"raw": fields.KeywordField()},
    )
    professional_tags = fields.TextField(
        analyzer=languages_analyzer,
        fields={"raw": fields.KeywordField()},
    )
    service_type = fields.TextField(
        analyzer=languages_analyzer,
        fields={"raw": fields.KeywordField()},
    )

    def prepare_tags(self, instance: Service) -> str:
        """Return the tags as a string."""
        # pylint: disable=no-self-use
        return " ".join([t.name for t in instance.tags.all()])

    def prepare_professional_name(self, instance: Service) -> str:
        """Return the professional name."""
        # pylint: disable=no-self-use
        return instance.professional.name

    def prepare_professional_description(self, instance: Service) -> str:
        """Return the professional description."""
        # pylint: disable=no-self-use
        return instance.professional.description

    def prepare_professional_tags(self, instance: Service) -> str:
        """Return the tags as a string."""
        # pylint: disable=no-self-use
        return " ".join([t.name for t in instance.professional.tags.all()])

    def prepare_service_type(self, instance: Service) -> str:
        """Return the tags as a string."""
        # pylint: disable=no-self-use
        return instance.get_service_type_display()

    class Index:
        """The index settings class."""

        name = "services"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        """The django settings class."""

        model = Service
        related_models = [ServiceTag, Professional, ProfessionalTag]

    def get_queryset(self) -> QuerySet:
        """Return the queryset."""
        return super().get_queryset().select_related("professional").\
            prefetch_related("tags")

    def get_instances_from_related(
        self,
        related_instance: ServiceTag,
    ) -> Service:
        """Get a service from the tag."""
        # pylint: disable=no-self-use
        if isinstance(related_instance, Professional):
            return related_instance.services.all()
        if isinstance(related_instance, ProfessionalTag):
            return related_instance.professional.services.all()
        return related_instance.service
