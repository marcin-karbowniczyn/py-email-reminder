from rest_framework import serializers
from core.models import Remainder


class RemainderSerializer(serializers.ModelSerializer):
    """ Serializer for Remainders """

    class Meta:
        model = Remainder
        fields = ['id', 'title', 'description', 'remainder_date', 'permanent']
