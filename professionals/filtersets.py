"""The professional filtersets module."""

from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from .models import Professional, ProfessionalTag


def _get_professionals(request: HttpRequest) -> QuerySet:
    """Get a list of professionals."""
    if not request:
        return Professional.objects.none()
    return Professional.objects.get_user_list(user=request.user)


class ProfessionalTagFilterSet(filters.FilterSet):
    """The filter class for the professional tag viewset class."""

    professional = filters.ModelChoiceFilter(
        label=_('professional'),
        queryset=_get_professionals,
    )

    @staticmethod
    class Meta:
        """The professional filterset class serializer META class."""

        model = ProfessionalTag
        fields = ('professional', )
