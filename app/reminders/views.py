from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Reminder, Tag
from reminders import serializers


class ReminderViewSet(viewsets.ModelViewSet):
    """ View for managing reminders API """
    queryset = Reminder.objects.all()
    # serializer_class = serializers.ReminderSerializer # We use get_serializer_class()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, query_string):
        """ Convert a list of strings to integers """
        return [int(str_id) for str_id in query_string.split(',')]

    def get_queryset(self):
        """ Retrieve only reminders of authenticated user """
        tags = self.request.query_params.get('tags')
        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.filter(user=self.request.user).order_by('-reminder_date').distinct()

    def get_serializer_class(self):
        """ Return the serializer class based on request action """
        if self.action == 'list':
            return serializers.ReminderSerializer
        return serializers.ReminderDetailSerializer

    def perform_create(self, serializer):
        """ Create a new reminder """
        serializer.save(user=self.request.user)


class TagViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """ View for managing Tags API """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve only tags of authenticated user """
        queryset = self.queryset
        assigned_only = bool(int(self.request.query_params.get('assigned_only', 0)))
        if assigned_only:
            queryset = queryset.filter(reminder__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-name').distinct()
