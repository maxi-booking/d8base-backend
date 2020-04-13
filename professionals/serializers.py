"""The users serializers module."""

from rest_framework import serializers

from .models import Category, Subcategory


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
