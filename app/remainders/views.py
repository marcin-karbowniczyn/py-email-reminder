from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Remainder
from remainders import serializers


class RemainderViewSet(viewsets.ModelViewSet):
    """ View for managing remainders API """
    queryset = Remainder.objects.all()
    # serializer_class = serializers.RemainderSerializer # We use get_serializer_class()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve only remainders of authenticated user """
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """ Return the serializer class based on request action """
        if self.action == 'list':
            return serializers.RemainderSerializer
        return serializers.RemainderDetailSerializer

    def perform_create(self, serializer):
        """ Create a new remainder """
        serializer.save(user=self.request.user)
