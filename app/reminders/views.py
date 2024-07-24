from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Reminder
from reminders import serializers


class ReminderViewSet(viewsets.ModelViewSet):
    """ View for managing reminders API """
    queryset = Reminder.objects.all()
    # serializer_class = serializers.ReminderSerializer # We use get_serializer_class()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve only reminders of authenticated user """
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """ Return the serializer class based on request action """
        if self.action == 'list':
            return serializers.ReminderSerializer
        return serializers.ReminderDetailSerializer

    def perform_create(self, serializer):
        """ Create a new reminder """
        serializer.save(user=self.request.user)
