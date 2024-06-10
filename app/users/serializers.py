""" Serializers for the Users API View """
from django.contrib.auth import get_user_model, authenticate
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

    # Overwrite update method to handle hashing password. Use parent's update method for other fields.
    def update(self, instance, validated_data):
        """ Update and return user """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password is not None:
            user.set_password(password)
            user.save()

        return user


# Custom Auth Token Serializer for using email instead of default username
class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user auth token """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, data):
        """ Validate and authenticate the user """
        email = data.get('email')
        password = data.get('password')
        user = authenticate(
            self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = 'Unable to authenticate with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
