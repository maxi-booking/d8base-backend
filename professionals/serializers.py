"""The users serializers module."""

from rest_framework import serializers

from users.serializers import UserHiddenFieldMixin

from .models import (Category, Professional, ProfessionalContact,
                     ProfessionalLocation, ProfessionalTag, Subcategory)


class AccountProfessionalForeignKey(serializers.PrimaryKeyRelatedField):
    """The professional field filtered by the request user."""

    def get_queryset(self):
        """Return the queryset."""
        user = self.context['request'].user
        return Professional.objects.get_user_list(user=user)


class ProfessionalLocationSerializer(
        serializers.ModelSerializer, ):
    """The professional location serializer."""

    professional = AccountProfessionalForeignKey()

    class Meta:
        """The professional location class serializer META class."""

        model = ProfessionalLocation

        fields = ('id', 'professional', 'country', 'region', 'subregion',
                  'city', 'district', 'postal_code', 'address', 'coordinates',
                  'units', 'timezone', 'created', 'modified', 'created_by',
                  'modified_by')
        read_only_fields = ('created', 'modified', 'created_by', 'modified_by')


class ProfessionalContactSerializer(
        serializers.ModelSerializer, ):
    """The professional contact serializer."""

    professional = AccountProfessionalForeignKey()

    class Meta:
        """The professional contact class serializer META class."""

        model = ProfessionalContact
        fields = ('id', 'professional', 'contact', 'contact_display', 'value', 'created',
                  'modified', 'created_by', 'modified_by')
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


class ProfessionalSerializer(
        UserHiddenFieldMixin,
        serializers.ModelSerializer,
):
    """The professional serializer."""

    class Meta:
        """The professional class serializer META class."""

        model = Professional
        fields = ('id', 'user', 'name', 'description', 'company', 'experience',
                  'level', 'is_auto_order_confirmation', 'subcategory',
                  'created', 'modified', 'created_by', 'modified_by')
        read_only_fields = ('created', 'modified', 'created_by', 'modified_by')


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
