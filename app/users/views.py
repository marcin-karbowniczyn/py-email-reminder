""" Views for the Users API """
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status

from users.serializers import (
    RegisterNewUserSerializer,
    ManageUserSerializer,
    ChangePasswordSerializer,
    DeleteMeSerializer,
    AuthTokenSerializer
)
from users.emails import welcome_email


class RegisterNewUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = RegisterNewUserSerializer

    def perform_create(self, serializer):
        """ Create a new user and send a welcoming e-mail """
        user = serializer.save()
        if user:
            welcome_email(user).send()


class CreateAuthTokenView(ObtainAuthToken):
    """ Create a new Auth Token for validated users """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the authenticated user """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ManageUserSerializer

    # Thanks to Token Auth, user will be added to the request
    def get_object(self):
        """ Retrieve and return the authenticated user """
        return self.request.user


class ChangeUserPasswordView(generics.UpdateAPIView):
    """ View for changing the authenticated user's password """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    # I had to override it to hide passwords from the reponse.
    # Default is 'return Response(serializer.data)'
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'msg': 'Password has been changed.'})

    def get_object(self):
        """ Retrieve and return the authenticated user """
        return self.request.user


class DeleteMeView(generics.DestroyAPIView):
    """ View for deleting the authenticated user """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeleteMeSerializer

    # I overidden this run serializer validators.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # We want to confirm password once again before the user is deleted.
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        """ Retrieve and return the authenticated user """
        return self.request.user
