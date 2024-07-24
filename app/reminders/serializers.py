from rest_framework import serializers
from core.models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    """ Serializer for Reminders """

    class Meta:
        model = Reminder
        fields = ['id', 'title', 'reminder_date', 'permanent']
        extra_kwargs = {'id': {'read_only': True}}  # Redundant, but I prefered to have this included


class ReminderDetailSerializer(ReminderSerializer):
    """ Serializer for detailed Reminders """

    class Meta(ReminderSerializer.Meta):
        fields = ReminderSerializer.Meta.fields + ['description']
