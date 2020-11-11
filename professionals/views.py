"""The professionals views module."""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from d8b.viewsets import AllowAnyViewSetMixin
from schedule.availability import generate_for_professional

from .filtersets import (
    ProfessionalCertificateFilterSet, ProfessionalContactFilterSet,
    ProfessionalEductationFilterSet, ProfessionalExperienceFilterSet,
    ProfessionalListFilterSet, ProfessionalLocationFilterSet,
    ProfessionalPhotoFilterSet, ProfessionalTagFilterSet)
from .models import (Category, Professional, ProfessionalCertificate,
                     ProfessionalContact, ProfessionalEducation,
                     ProfessionalExperience, ProfessionalLocation,
                     ProfessionalPhoto, ProfessionalTag, Subcategory)
from .serializers import (
    CategorySerializer, ProfessionalCertificateSerializer,
    ProfessionalContactSerializer, ProfessionalEducationSerializer,
    ProfessionalExperienceSerializer, ProfessionalListSerializer,
    ProfessionalLocationSerializer, ProfessionalPhotoListSerializer,
    ProfessionalPhotoSerializer, ProfessionalSerializer,
    ProfessionalTagListSerializer, ProfessionalTagSerializer,
    SubcategorySerializer)


class ProfessionalLocationViewSet(viewsets.ModelViewSet):
    """The professional contact viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "professional__user"
    serializer_class = ProfessionalLocationSerializer
    queryset = ProfessionalLocation.objects.get_list()
    filterset_class = ProfessionalLocationFilterSet


class ProfessionalContactViewSet(viewsets.ModelViewSet):
    """The professional contact viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "professional__user"
    serializer_class = ProfessionalContactSerializer
    queryset = ProfessionalContact.objects.get_list()
    search_fields = ("=id", "contact__name", "value")
    filterset_class = ProfessionalContactFilterSet


class ProfessionalEducationViewSet(viewsets.ModelViewSet):
    """The professional education viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "professional__user"
    serializer_class = ProfessionalEducationSerializer
    queryset = ProfessionalEducation.objects.get_list()
    search_fields = ("=id", "university", "deegree", "field_of_study")
    filterset_class = ProfessionalEductationFilterSet


class ProfessionalPhotoViewSet(viewsets.ModelViewSet):
    """The professional photo viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "professional__user"
    serializer_class = ProfessionalPhotoSerializer
    queryset = ProfessionalPhoto.objects.get_list()
    search_fields = ("=id", "name", "description")
    filterset_class = ProfessionalPhotoFilterSet


class ProfessionalPhotoListViewSet(viewsets.ReadOnlyModelViewSet):
    """The professional photo list viewset."""

    serializer_class = ProfessionalPhotoListSerializer
    queryset = ProfessionalPhoto.objects.get_list()
    search_fields = ("=id", "name", "description")
    filterset_fields = ("professional", )


class ProfessionalCertificateViewSet(viewsets.ModelViewSet):
    """The professional certificate viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "professional__user"
    serializer_class = ProfessionalCertificateSerializer
    queryset = ProfessionalCertificate.objects.get_list()
    search_fields = ("=id", "name", "organization")
    filterset_class = ProfessionalCertificateFilterSet


class ProfessionalExperienceViewSet(viewsets.ModelViewSet):
    """The professional education viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "professional__user"
    serializer_class = ProfessionalExperienceSerializer
    queryset = ProfessionalExperience.objects.get_list()
    search_fields = ("=id", "title", "company")
    filterset_class = ProfessionalExperienceFilterSet


class ProfessionalTagViewSet(viewsets.ModelViewSet):
    """The professional tag viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "professional__user"
    serializer_class = ProfessionalTagSerializer
    queryset = ProfessionalTag.objects.get_list()
    search_fields = ("=id", "name")
    filterset_class = ProfessionalTagFilterSet


class ProfessionalTagListViewSet(viewsets.ReadOnlyModelViewSet):
    """The professional tag list viewset."""

    serializer_class = ProfessionalTagListSerializer
    queryset = ProfessionalTag.objects.get_names()
    search_fields = ("name", )


class ProfessionalListViewSet(viewsets.ReadOnlyModelViewSet):
    """The professional list viewset."""

    serializer_class = ProfessionalListSerializer
    queryset = Professional.objects.get_extended_list()
    search_fields = ("=id", "name", "user__email")
    filterset_class = ProfessionalListFilterSet


class ProfessionalViewSet(viewsets.ModelViewSet):
    """The professional viewset."""

    is_owner_filter_enabled = True
    serializer_class = ProfessionalSerializer
    queryset = Professional.objects.get_list()
    search_fields = ("=id", "name")

    @action(detail=True, methods=["post"])
    def generate_calendar(self, request, pk=None):
        # pylint: disable=unused-argument
        """Generate the professional calendar."""
        generate_for_professional(self.get_object())
        return Response({"status": "ok"})


class CategoryViewSet(
        CacheResponseMixin,
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The category viewset."""

    serializer_class = CategorySerializer
    queryset = Category.objects.get_list()
    search_fields = ("=id", "name")


class SubcategoryViewSet(
        CacheResponseMixin,
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The subcategory viewset."""

    serializer_class = SubcategorySerializer
    queryset = Subcategory.objects.get_list()
    search_fields = ("=id", "name", "category__name")
    filterset_fields = ("category", )
