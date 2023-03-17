"""
Database models.
"""
from django.contrib.auth.models import User
from django.db import models
from bitfield import BitField


class Place(models.Model):
    """Place object."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)

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
