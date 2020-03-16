"""The users serializers module."""
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """The User class serializer."""

    class Meta:
        """The User class serializer META class."""

        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'patronymic', 'phone',
            'gender', 'birthday', 'account_type', 'is_staff', 'is_active',
            'date_joined'
        ]
