"""
Tests for lunch APIs.
"""
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Place

from lunch.serializers import (
    PlaceSerializer,
    PlaceDetailSerializer
)


PLACES_URL = reverse('lunch:place-list')


def detail_url(place_id):
    """Create and return a place detail URL."""
    return reverse('lunch:place-detail', args=[place_id])


def image_upload_url(place_id):
    """Create and return an image upload URL."""
    return reverse('lunch:place-upload-image', args=[place_id])


def create_place(**params):
    """Create and return a sample place."""
    defaults = {
        'name': 'Good restaurant',
        'address': 'Route 66',
        'lat': '10.234',
        'lon': '22.678'
    }
    defaults.update(params)

    place = Place.objects.create(**defaults)
    return place


class PublicPlaceAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PLACES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePlaceApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='TestName',
            email='test@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_places(self):
        """Test retrieving a list of places."""
        create_place()
        create_place()

        res = self.client.get(PLACES_URL)

        places = Place.objects.all().order_by('name')
        serializer = PlaceSerializer(places, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_place_detail(self):
        """Test get place detail."""
        place = create_place()

        url = detail_url(place.id)
        res = self.client.get(url)

        serializer = PlaceDetailSerializer(place)
        self.assertEqual(res.data, serializer.data)

    def test_create_place(self):
        """Test creating a place."""
        payload = {
            'name': 'Sample restaurant',
            'address': 'Route 66',
        }
        res = self.client.post(PLACES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        place = Place.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(place, k), v)

    def test_partial_update(self):
        """Test partial update of a place."""
        original_name = 'Sample restaurant'
        place = create_place(
            name=original_name,
            address='Route 66',
        )

        payload = {'address': 'Route 67'}
        url = detail_url(place.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        place.refresh_from_db()
        self.assertEqual(place.address, payload['address'])
        self.assertEqual(place.name, original_name)

    def test_full_update(self):
        """Test full update of place."""
        place = create_place(
            name='Sample restaurant',
            address='Route 66',
        )

        payload = {
            'name': 'Sample restaurant 2',
            'address': 'Route 67',
        }
        url = detail_url(place.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        place.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(place, k), v)

    def test_delete_place(self):
        """Test deleting a place successful."""
        place = create_place()

        url = detail_url(place.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Place.objects.filter(id=place.id).exists())

    def test_search_place(self):
        """Test searching a place for name and address."""
        p1 = create_place()
        p2 = create_place(
            name='Street food',
            address='Street foot',
        )
        s1 = PlaceSerializer(p1)
        s2 = PlaceSerializer(p2)

        params = {'search': 'rest'}
        res = self.client.get(PLACES_URL, params)

        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

        params = {'search': 'foot'}
        res = self.client.get(PLACES_URL, params)

        self.assertNotIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)

    def test_place_retrieve_limited(self):
        """Test retrieving a limited list of places."""
        p1 = create_place()
        p2 = create_place(
            name='Street food',
            address='Street foot',
        )
        s1 = PlaceSerializer(p1)
        s2 = PlaceSerializer(p2)

        params = {'limit': 1}
        res = self.client.get(PLACES_URL, params)

        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_place_retrieve_starting_from_offset(self):
        """Test retrieving a places starting from offset."""
        p1 = create_place()
        p2 = create_place(
            name='Street food',
            address='Street foot',
        )
        s1 = PlaceSerializer(p1)
        s2 = PlaceSerializer(p2)

        params = {'offset': 1}
        res = self.client.get(PLACES_URL, params)

        self.assertNotIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)

    def test_place_retrieve_limited_invalid_limit(self):
        for x in range(2000):
            create_place()

        params = {'limit': 0}
        res = self.client.get(PLACES_URL, params)

        self.assertEqual(len(res.data), 1000)

        params = {'limit': 2000}
        res = self.client.get(PLACES_URL, params)

        self.assertEqual(len(res.data), 1000)


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='TestName',
            email='test@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)
        self.place = create_place()

    def tearDown(self):
        self.place.image.delete()

    def test_upload_image(self):
        """Test uploading an image to a place."""
        url = image_upload_url(self.place.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.place.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.place.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image."""
        url = image_upload_url(self.place.id)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
