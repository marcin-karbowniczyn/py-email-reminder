""" Views for the Users API """
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from users.serializers import (
    RegisterNewUserSerializer,
    ManageUserSerializer,
    ChangePasswordSerializer,
    AuthTokenSerializer
)


class RegisterNewUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = RegisterNewUserSerializer


class CreateAuthTokenView(ObtainAuthToken):
    """ Create a new Auth Token for validated users """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ChangeUserPasswordView(generics.UpdateAPIView):
    """ View for changing the authenticated user's password """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        """ Retrieve and return the authenticated user """
        return self.request.user


# Think about how to handle deleting users, I should ask them for password. Another separate View?
# Maybe something like me/delete?
class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """ Manage the authenticated user """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ManageUserSerializer

    # Thanks to Token Auth, user will be added to the request
    def get_object(self):
        """ Retrieve and return the authenticated user """
        return self.request.user
