""" Views for the Users API """
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from users.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView, generics.UpdateAPIView):
    """ Create a new user in the system """
    serializer_class = UserSerializer


class CreateAuthTokenView(ObtainAuthToken):
    """ Create a new Auth Token for validated users """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """ Manage the authenticated user """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    # Thanks to Token Auth, user will be added to the request
    def get_object(self):
        """ Retrieve and return the authenticated user """
        return self.request.user
