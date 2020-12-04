"""The d8b pagination module."""

from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """The standart pagination class."""

    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 1000

    @staticmethod
    def get_schema_serializer(response_serializer):
        """Get the paginated result serializer."""

        class PaginatedResultSerializer(serializers.Serializer):
            """The pagination serializer."""

            # pylint: disable=abstract-method
            count = serializers.IntegerField(read_only=True)
            next = serializers.CharField(read_only=True)
            previous = serializers.CharField(read_only=True)
            results = response_serializer(many=True, read_only=True)

        return PaginatedResultSerializer(many=False)
