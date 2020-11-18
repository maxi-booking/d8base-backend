"""The d8b serializers module."""
from copy import deepcopy

from rest_framework import serializers


class ModelCleanFieldsSerializer(serializers.ModelSerializer):
    """The serializer to call the model clean method."""

    def validate(self, attrs):
        """Validate the object."""
        # pylint: disable=no-member
        if not self.instance:
            self.Meta.model(**attrs).full_clean()
        else:
            instance = deepcopy(self.instance)
            for key, value in attrs.items():
                setattr(instance, key, value)
            instance.clean()
        return super().validate(attrs)
