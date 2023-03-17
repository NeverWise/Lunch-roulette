"""
Serializers for lunch APIs
"""
from rest_framework import serializers

from core.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer for places."""

    class Meta:
        model = Place
        fields = ['id', 'name', 'address']
        read_only_fields = ['id']
