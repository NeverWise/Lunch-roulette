"""
Tests for models.
"""
from django.test import TestCase

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_place(self):
        """Test creating a place is successful."""
        place = models.Place.objects.create(
            name='Sample resturant name',
            address='Sample receipe description',
        )

        self.assertEqual(str(place), place.name)
