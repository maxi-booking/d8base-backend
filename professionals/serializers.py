"""The professionals serializers module."""

from typing import Tuple

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from d8b.serializers import ModelCleanFieldsSerializer
from users.serializer_fields import AccountUserLocationForeignKey
from users.serializers import UserExtendedSerializer, UserHiddenFieldMixin

from .models import (Category, Professional, ProfessionalCertificate,
                     ProfessionalContact, ProfessionalEducation,
                     ProfessionalExperience, ProfessionalLocation,
                     ProfessionalPhoto, ProfessionalTag, Subcategory)
from .serializer_fields import AccountProfessionalForeignKey


class ProfessionalLocationSerializer(ModelCleanFieldsSerializer):
    """The professional location serializer."""

    professional = AccountProfessionalForeignKey()
    user_location = AccountUserLocationForeignKey(required=False)

    class Meta:
        """The professional location class serializer META class."""

        model = ProfessionalLocation

        fields = ("id", "professional", "user_location", "country", "region",
                  "subregion", "city", "district", "postal_code", "address",
                  "coordinates", "units", "timezone", "created", "modified",
                  "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ProfessionalLocationInlineSerializer(serializers.ModelSerializer):
    """The professional inline location serializer."""

    class Meta:
        """The metainformation."""

        model = ProfessionalLocation

        fields = ("id", "country", "region", "subregion", "city", "district",
                  "postal_code", "address", "coordinates", "units", "timezone")


class ProfessionalContactSerializer(serializers.ModelSerializer):
    """The professional contact serializer."""

    professional = AccountProfessionalForeignKey()

    class Meta:
        """The professional contact class serializer META class."""

        model = ProfessionalContact
        fields = ("id", "professional", "contact", "contact_display", "value",
                  "created", "modified", "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ProfessionalContactInlineSerializer(serializers.ModelSerializer):
    """The professional inline contact serializer."""

    class Meta:
        """The professional contact class serializer META class."""

        model = ProfessionalContact
        fields = ("id", "contact", "contact_display", "value")


class ProfessionalTagSerializer(serializers.ModelSerializer):
    """The professional tag serializer."""

    professional = AccountProfessionalForeignKey()

    class Meta:
        """The professional tag class serializer META class."""

        model = ProfessionalTag
        fields = ("id", "professional", "name", "created", "modified",
                  "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ProfessionalTagListSerializer(serializers.ModelSerializer):
    """The professional tag list serializer."""

    class Meta:
        """The professional class serializer META class."""

        model = ProfessionalTag
        fields = ("name", )


class ProfessionalExperienceSerializer(ModelCleanFieldsSerializer):
    """The professional experience serializer."""

    professional = AccountProfessionalForeignKey()

    class Meta:
        """The metainformation."""

        model = ProfessionalExperience
        fields = ("id", "professional", "title", "company", "is_still_here",
                  "start_date", "end_date", "description", "created",
                  "modified", "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ProfessionalExperienceInlineSerializer(serializers.ModelSerializer):
    """The professional inline experience serializer."""

    class Meta:
        """The metainformation."""

        model = ProfessionalExperience
        fields = ("id", "title", "company", "is_still_here", "start_date",
                  "end_date", "description")


class ProfessionalEducationSerializer(ModelCleanFieldsSerializer):
    """The professional education serializer."""

    professional = AccountProfessionalForeignKey()

    class Meta:
        """The metainformation."""

        model = ProfessionalEducation
        fields = ("id", "professional", "university", "deegree",
                  "field_of_study", "is_still_here", "start_date", "end_date",
                  "description", "created", "modified", "created_by",
                  "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ProfessionalEducationInlineSerializer(ModelCleanFieldsSerializer):
    """The professional inline education serializer."""

    class Meta:
        """The metainformation."""

        model = ProfessionalEducation
        fields = ("id", "university", "deegree", "field_of_study",
                  "is_still_here", "start_date", "end_date", "description")


class ProfessionalCertificateSerializer(ModelCleanFieldsSerializer):
    """The professional certificate serializer."""

    professional = AccountProfessionalForeignKey()

    photo_thumbnail = serializers.ImageField(read_only=True)
    photo = Base64ImageField(required=False)

    class Meta:
        """The metainformation."""

        model = ProfessionalCertificate
        fields = ("id", "professional", "name", "organization", "date",
                  "certificate_id", "url", "photo", "photo_thumbnail",
                  "created", "modified", "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ProfessionalCertificateInlineSerializer(ModelCleanFieldsSerializer):
    """The professional inline certificate serializer."""

    photo_thumbnail = serializers.ImageField(read_only=True)
    photo = Base64ImageField(required=False, read_only=True)

    class Meta:
        """The metainformation."""

        model = ProfessionalCertificate
        fields = ("id", "name", "organization", "date", "certificate_id",
                  "url", "photo", "photo_thumbnail")


class ProfessionalListSerializer(serializers.ModelSerializer):
    """The professional list serializer."""

    user = UserExtendedSerializer(many=False, read_only=True)
    tags = ProfessionalTagListSerializer(many=True, read_only=True)
    contacts = ProfessionalContactInlineSerializer(many=True, read_only=True)
    locations = ProfessionalLocationInlineSerializer(many=True, read_only=True)
    experience_entries = ProfessionalExperienceInlineSerializer(
        many=True,
        read_only=True,
    )
    educations = ProfessionalEducationInlineSerializer(
        many=True,
        read_only=True,
    )
    certificates = ProfessionalCertificateInlineSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        """The professional list class serializer META class."""

        model = Professional
        fields: Tuple[str, ...] = (
            "id",
            "user",
            "name",
            "description",
            "company",
            "level",
            "rating",
            "subcategory",
            "experience",
            "tags",
            "contacts",
            "locations",
            "experience_entries",
            "educations",
            "certificates",
            "created",
            "modified",
        )
        read_only_fields = ("rating", "created", "modified")


class ProfessionalSerializer(
        UserHiddenFieldMixin,
        ProfessionalListSerializer,
        serializers.ModelSerializer,
):
    """The professional serializer."""

    class Meta(ProfessionalListSerializer.Meta):
        """The professional class serializer META class."""

        fields = ("id", "user", "name", "description", "company", "level",
                  "rating", "subcategory", "experience", "created", "modified")


class CategorySerializer(serializers.ModelSerializer):
    """The category serializer."""

    class Meta:
        """The category class serializer META class."""

        model = Category
        fields = ("id", "name", "description", "order")
        read_only_fields = ("order", )


class SubcategorySerializer(serializers.ModelSerializer):
    """The subcategory serializer."""

    class Meta:
        """The subcategory class serializer META class."""

        model = Subcategory
        fields = ("id", "category", "name", "description", "order")
        read_only_fields = ("order", )


class ProfessionalPhotoSerializer(ModelCleanFieldsSerializer):
    """The professional photo serializer."""

    professional = AccountProfessionalForeignKey()

    photo_thumbnail = serializers.ImageField(read_only=True)
    photo = Base64ImageField(required=True)

    class Meta:
        """The metainformation."""

        model = ProfessionalPhoto
        fields = ("id", "professional", "name", "description", "order",
                  "photo", "photo_thumbnail", "created", "modified",
                  "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ProfessionalPhotoListSerializer(serializers.ModelSerializer):
    """The professional photo list serializer."""

    photo_thumbnail = serializers.ImageField(read_only=True)
    photo = Base64ImageField(required=False, read_only=True)

    class Meta:
        """The metainformation."""

        model = ProfessionalPhoto
        fields = ("id", "professional", "name", "description", "order",
                  "photo", "photo_thumbnail", "created", "modified")
        read_only_fields = ("created", "modified")
