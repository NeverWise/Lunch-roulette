"""
Serializers for lunch APIs
"""
from rest_framework import serializers

from core.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer for places."""

    class Meta:
        model = Place
        fields = ['id', 'name', 'address', 'image']
        read_only_fields = ['id']


class PlaceDetailSerializer(PlaceSerializer):
    """Serializer for place detail view."""

    class Meta(PlaceSerializer.Meta):
        fields = PlaceSerializer.Meta.fields + ['lat', 'lon']


class PlaceImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to places."""

    class Meta:
        model = Place
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}
