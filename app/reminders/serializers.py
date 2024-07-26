from rest_framework import serializers
from core.models import Reminder, Tag


# From Django documentation:
#  The default implementation also does not handle nested relationships.
#  If you want to support writable nested relationships you'll need to write an explicit `.create()` method.


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for Tags """

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class ReminderSerializer(serializers.ModelSerializer):
    """ Serializer for Reminders """
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Reminder
        fields = ['id', 'title', 'reminder_date', 'permanent', 'tags']
        extra_kwargs = {'id': {'read_only': True}}  # Redundant, but I prefered to have this included

    # M2M fields are read only by default
    def create(self, validated_data):
        """ Create a Reminder """
        # 1. Remove tags from validated data and return them
        tags = validated_data.pop('tags', [])

        # 2. Create a new reminder with the rest of data
        reminder = Reminder.objects.create(**validated_data)  # Sprawdzić self.Meta.objects

        # 3.Get authenticated user from the request and liip through tags from validated data
        auth_user = self.context['request'].user
        for tag in tags:
            tag['name'] = ' '.join(tag['name'].split()).title()
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)
            reminder.tags.add(tag_obj)

        return reminder

    def update(self, instance, validated_data):
        """ Update a Reminder """
        tags = validated_data.pop('tags', None)

        if tags is not None:
            instance.tags.clear()
            auth_user = self.context['request'].user
            for tag in tags:
                tag['name'] = ' '.join(tag['name'].split()).title()
                tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)
                instance.tags.add(tag_obj)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ReminderDetailSerializer(ReminderSerializer):
    """ Serializer for detailed Reminders """

    class Meta(ReminderSerializer.Meta):
        fields = ReminderSerializer.Meta.fields + ['description']
