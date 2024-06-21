from rest_framework import serializers
from core.models import Remainder


class RemainderSerializer(serializers.ModelSerializer):
    """ Serializer for Remainders """

    class Meta:
        model = Remainder
        fields = ['id', 'title', 'remainder_date', 'permanent']
        extra_kwargs = {'id': {'read_only': True}}  # Redundant, but I prefered to have this included


class RemainderDetailSerializer(RemainderSerializer):
    """ Serializer for detailed Remainders """

    class Meta(RemainderSerializer.Meta):
        fields = RemainderSerializer.Meta.fields + ['description']
