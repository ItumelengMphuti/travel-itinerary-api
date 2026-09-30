from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Itinerary


User = get_user_model()


class ItineraryAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123",
        )

        self.client.force_authenticate(user=self.user)

    def test_create_itinerary(self):
        data = {
            "title": "Cape Town Trip",
            "description": "A trip to Cape Town",
            "start_date": "2026-10-01",
            "end_date": "2026-10-05",
            "status": "planning",
        }

        response = self.client.post(
            "/api/itineraries/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Itinerary.objects.count(), 1)

    def test_unauthenticated_user_cannot_create_itinerary(self):
        self.client.force_authenticate(user=None)

        data = {
            "title": "Unauthorised Trip",
            "description": "Should not be created",
            "start_date": "2026-10-01",
            "end_date": "2026-10-05",
            "status": "planning",
        }

        response = self.client.post(
            "/api/itineraries/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_dates_are_rejected(self):
        data = {
            "title": "Invalid Trip",
            "description": "Invalid dates",
            "start_date": "2026-10-10",
            "end_date": "2026-10-05",
            "status": "planning",
        }

        response = self.client.post(
            "/api/itineraries/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)