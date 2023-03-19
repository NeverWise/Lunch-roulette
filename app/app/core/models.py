"""
Database models.
"""
import uuid
import os

from django.contrib.auth.models import User
from django.db import models
from bitfield import BitField


def place_image_file_path(instance, filename):
    """Generate file path for new place image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'place', filename)


class Place(models.Model):
    """Place object."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    lat = models.CharField(max_length=100, blank=True)
    lon = models.CharField(max_length=100, blank=True)
    image = models.ImageField(null=True, upload_to=place_image_file_path)

    def __str__(self):
        return self.name


class Setting(models.Model):
    """Setting object."""
    name = models.CharField(max_length=255)
    colleagues_number = models.SmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    week_days = BitField(flags=(
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
    ))

    def __str__(self):
        return self.name


class Event(models.Model):
    """Event object."""
    name = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    colleagues = models.ManyToManyField(User)

    def __str__(self):
        return self.name
