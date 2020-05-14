"""The users serializers module."""

from rest_framework import serializers

from d8b.serializers import ModelCleanFieldsSerializer
from users.serializer_fields import AccountUserLocationForeignKey
from users.serializers import UserHiddenFieldMixin

from .models import (Category, Professional, ProfessionalContact,
                     ProfessionalLocation, ProfessionalTag, Subcategory)
from .serializer_fields import AccountProfessionalForeignKey


class ProfessionalLocationSerializer(ModelCleanFieldsSerializer):
    """The professional location serializer."""

    professional = AccountProfessionalForeignKey()
    user_location = AccountUserLocationForeignKey(required=False)

    class Meta:
        """The professional location class serializer META class."""

        model = ProfessionalLocation

        fields = ('id', 'professional', 'user_location', 'country', 'region',
                  'subregion', 'city', 'district', 'postal_code', 'address',
                  'coordinates', 'units', 'timezone', 'created', 'modified',
                  'created_by', 'modified_by')
        read_only_fields = ('created', 'modified', 'created_by', 'modified_by')


class ProfessionalContactSerializer(
        serializers.ModelSerializer, ):
    """The professional contact serializer."""

    professional = AccountProfessionalForeignKey()

    class Meta:
        """The professional contact class serializer META class."""

        model = ProfessionalContact
        fields = ('id', 'professional', 'contact', 'contact_display', 'value',
                  'created', 'modified', 'created_by', 'modified_by')
        read_only_fields = ('created', 'modified', 'created_by', 'modified_by')


class ProfessionalTagSerializer(
        serializers.ModelSerializer, ):
    """The professional tag serializer."""

    professional = AccountProfessionalForeignKey()

    class Meta:
        """The professional tag class serializer META class."""

        model = ProfessionalTag
        fields = ('id', 'professional', 'name', 'created', 'modified',
                  'created_by', 'modified_by')
        read_only_fields = ('created', 'modified', 'created_by', 'modified_by')


class ProfessionalTagListSerializer(
        serializers.ModelSerializer, ):
    """The professional tag list serializer."""

    class Meta:
        """The professional class serializer META class."""

        model = ProfessionalTag
        fields = ('name', )


class ProfessionalListSerializer(serializers.ModelSerializer):
    """The professional list serializer."""

    class Meta:
        """The professional list class serializer META class."""

        model = Professional
        fields = ('id', 'user', 'name', 'description', 'company', 'experience',
                  'level', 'is_auto_order_confirmation', 'subcategory',
                  'created', 'modified', 'created_by', 'modified_by')
        read_only_fields = ('created', 'modified', 'created_by', 'modified_by')


class ProfessionalSerializer(
        ProfessionalListSerializer,
        UserHiddenFieldMixin,
        serializers.ModelSerializer,
):
    """The professional serializer."""

    class Meta(ProfessionalListSerializer.Meta):
        """The professional class serializer META class."""


class CategorySerializer(serializers.ModelSerializer):
    """The category serializer."""

    class Meta:
        """The category class serializer META class."""

        model = Category
        fields = ('id', 'name', 'description', 'order')
        read_only_fields = ('order', )


class SubcategorySerializer(serializers.ModelSerializer):
    """The subcategory serializer."""

    class Meta:
        """The subcategory class serializer META class."""

        model = Subcategory
        fields = ('id', 'category', 'name', 'description', 'order')
        read_only_fields = ('order', )
