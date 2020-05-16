"""The professional filtersets module."""

from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from d8b.filtersets import NumberInFilter

from .models import (Professional, ProfessionalCertificate,
                     ProfessionalContact, ProfessionalEducation,
                     ProfessionalExperience, ProfessionalLocation,
                     ProfessionalTag)


def _get_professionals(request: HttpRequest) -> QuerySet:
    """Get a list of professionals."""
    if not request:
        return Professional.objects.none()
    return Professional.objects.get_user_list(user=request.user)


class ProfessionalListFilterSet(filters.FilterSet):
    """The filter class for the professional list viewset class."""

    pk_in = NumberInFilter(field_name='id', lookup_expr='in')
    experience = filters.NumericRangeFilter(
        field_name='experience',
        lookup_expr='range',
    )

    class Meta:
        """The professional list filterset class serializer META class."""

        model = Professional
        fields = ('pk_in', 'subcategory', 'subcategory__category', 'level')


class ProfessionalLocationFilterSet(filters.FilterSet):
    """The filter class for the professional location viewset class."""

    professional = filters.ModelChoiceFilter(
        label=_('professional'),
        queryset=_get_professionals,
    )

    class Meta:
        """The professional filterset class serializer META class."""

        model = ProfessionalLocation
        fields = ('professional', )


class ProfessionalCertificateFilterSet(filters.FilterSet):
    """The filter class for the professional certificate viewset class."""

    professional = filters.ModelChoiceFilter(
        label=_('professional'),
        queryset=_get_professionals,
    )

    class Meta:
        """The metainformation."""

        model = ProfessionalCertificate
        fields = ('professional', )


class ProfessionalExperienceFilterSet(filters.FilterSet):
    """The filter class for the professional experience viewset class."""

    professional = filters.ModelChoiceFilter(
        label=_('professional'),
        queryset=_get_professionals,
    )

    class Meta:
        """The metainformation."""

        model = ProfessionalExperience
        fields = ('professional', )


class ProfessionalEductationFilterSet(filters.FilterSet):
    """The filter class for the professional education viewset class."""

    professional = filters.ModelChoiceFilter(
        label=_('professional'),
        queryset=_get_professionals,
    )

    class Meta:
        """The metainformation."""

        model = ProfessionalEducation
        fields = ('professional', )


class ProfessionalContactFilterSet(filters.FilterSet):
    """The filter class for the professional contact viewset class."""

    professional = filters.ModelChoiceFilter(
        label=_('professional'),
        queryset=_get_professionals,
    )

    class Meta:
        """The professional filterset class serializer META class."""

        model = ProfessionalContact
        fields = ('professional', )


class ProfessionalTagFilterSet(filters.FilterSet):
    """The filter class for the professional tag viewset class."""

    professional = filters.ModelChoiceFilter(
        label=_('professional'),
        queryset=_get_professionals,
    )

    class Meta:
        """The professional filterset class serializer META class."""

        model = ProfessionalTag
        fields = ('professional', )
