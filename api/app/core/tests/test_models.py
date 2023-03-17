"""
Tests for models.
"""
from django.test import TestCase

from core import models

import datetime


class ModelTests(TestCase):
    """Test models."""

    def test_create_place(self):
        """Test creating a Place is successful."""
        place = models.Place.objects.create(
            name='Sample resturant name',
            address='Sample receipe description',
        )

        self.assertEqual(str(place), place.name)

    def test_create_setting(self):
        """Test creating a Setting is successful."""
        setting = models.Setting.objects.create(
            name='Default',
            colleagues_number=5,
            start_time=datetime.time(13, 0, 0),
            end_time=datetime.time(14, 0, 0),
            week_days=models.Setting.week_days.wednesday,
        )

        self.assertEqual(str(setting), setting.name)

    def test_create_event(self):
        """Test creating a Setting is successful."""
        place = models.Place.objects.create(
            name='Sample resturant name',
            address='Sample receipe description',
        )
        event = models.Event.objects.create(
            name='Lunch of today',
            date=datetime.date(2023, 4, 23),
            start_time=datetime.time(13, 0, 0),
            end_time=datetime.time(14, 0, 0),
            place=place,
        )
        event.colleagues.create(email='test@example.com',
                                password='testpass123',
                                username='TestName')
        event.colleagues.create(email='test2@example.com',
                                password='testpass123',
                                username='TestName2')

        self.assertEqual(str(event), event.name)
        self.assertEqual(str(event.place), place.name)
        self.assertEqual(event.colleagues.count(), 2)
