"""
Database models.
"""
from django.db import models


class Place(models.Model):
    """Place object."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
