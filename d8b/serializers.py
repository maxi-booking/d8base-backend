"""The d8b serializers module."""

from rest_framework import serializers


#TODO: test it
class ModelCleanFieldsSerializer(
        serializers.ModelSerializer, ):
    """The serializer to call the model clean method."""

    def validate(self, attrs):
        """Validate the object."""
        # pylint: disable=no-member
        instance = self.Meta.model(**attrs)
        instance.clean()
        return super().validate(attrs)
