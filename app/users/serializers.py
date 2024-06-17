""" Serializers for the Users API View """
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
# from django.db.utils import IntegrityError

from rest_framework import serializers


def validate_passwords(password, password_confirm):
    """ Validate passwords are the same, and password meets requirements """
    if password == password_confirm:
        try:
            password_validation.validate_password(password)
        except ValidationError as err:
            raise serializers.ValidationError(str(err))
    else:
        raise serializers.ValidationError("Passwords don't match.")


class RegisterNewUserSerializer(serializers.Serializer):
    """ Serializer for registering the new user """
    email = serializers.EmailField(max_length=255, required=True)
    name = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True, trim_whitespace=False)
    password_confirm = serializers.CharField(max_length=128, required=True, write_only=True, trim_whitespace=False)

    def validate(self, data):
        # Check if email exists (Django automatically responds with IntegrityError)
        # user = get_user_model().objects.filter(email=data['email'])
        # if user:
        #     raise IntegrityError({'email_error': 'User with this email already exists.'})

        # Validate passwords
        password = data.get('password')
        password_confirm = data.pop('password_confirm', '')
        validate_passwords(password, password_confirm)

        return data

    def create(self, validated_data):
        """ Create and return a user with encrypted password """
        return get_user_model().objects.create_user(**validated_data)


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


class ChangePasswordSerializer(serializers.Serializer):
    """ Serializer for changing authenticated user's password """
    password = serializers.CharField(max_length=128, required=True, trim_whitespace=False)
    password_confirm = serializers.CharField(max_length=128, required=True, write_only=True, trim_whitespace=False)

    def validate(self, data):
        """ Validate if passwords are the same and if new password meet requirements """
        # 1. Get password from request data and remove password_confirm from the request
        password = data.get('password')
        password_confirm = data.pop('password_confirm', '')

        # 2. Validate passwords
        validate_passwords(password, password_confirm)

        # 3. Return data
        return data

    # Overwrite update method to handle hashing password. Use parent's update method for other fields.
    def update(self, instance, validated_data):
        """ Update and return user """
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ManageUserSerializer(serializers.ModelSerializer):
    """ Serializer for changing safe User fields, don't use it for passwords """

    class Meta:
        model = get_user_model()
        fields = ['email', 'name']


class DeleteMeSerializer(serializers.Serializer):
    """ Serializer for deleting authenticated user """
    password = serializers.CharField(max_length=128, required=True, trim_whitespace=False)

    def validate_password(self, value):
        """ Check if user's password is correct """
        user = self.context['request'].user
        if user.check_password(value) is False:
            raise ValidationError('Incorrect password. Please try again.')

        return value
