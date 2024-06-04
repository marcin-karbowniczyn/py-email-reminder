""" Serializers for the Users API View """
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object """

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        """ Apply custom password validators """
        try:
            password_validation.validate_password(value)
        except ValidationError as err:
            raise serializers.ValidationError(str(err))

        return value

    def create(self, validated_data):
        """ Create and return a user with encrypted password """
        return get_user_model().objects.create_user(**validated_data)
