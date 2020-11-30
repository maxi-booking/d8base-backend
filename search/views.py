"""The search views module."""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from d8b.viewsets import AllowAnyViewSetMixin
from search.engine import get_search_engine
from search.engine.exceptions import SearchError
from search.engine.request import HTTPToSearchRequestConverter

from .schemes import SearchSchema
from .serializers import SearchSerializer


class SearchViewSet(AllowAnyViewSetMixin, viewsets.ViewSet):
    """The search viewset."""

    serializer_class = SearchSerializer

    @swagger_auto_schema(**SearchSchema.list_schema)
    def list(self, request: Request):
        """Return the professional calendar."""
        try:
            converter = HTTPToSearchRequestConverter(request)
            search_request = converter.get()
            engine = get_search_engine()
            response = engine.get(search_request)
            serializer = self.serializer_class(
                instance=response,
                many=True,
                context={"request": request},
            )
        except SearchError as error:
            raise ValidationError({"error": str(error)}) from error

        return Response(serializer.data)
