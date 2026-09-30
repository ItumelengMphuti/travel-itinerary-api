from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Itinerary, ItineraryParticipant

User = get_user_model()


class ItineraryAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="TestPassword123",
        )

        self.client.force_authenticate(user=self.user)

        self.itinerary = Itinerary.objects.create(
            user=self.user,
            title="Cape Town Trip",
            description="A trip to Cape Town",
            start_date="2026-10-01",
            end_date="2026-10-05",
            status="planning",
        )

    def test_create_itinerary(self):
        data = {
            "title": "Durban Trip",
            "description": "A trip to Durban",
            "start_date": "2026-11-01",
            "end_date": "2026-11-05",
            "status": "planning",
        }

        response = self.client.post(
            "/api/itineraries/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Itinerary.objects.count(),
            2,
        )

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

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

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

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_list_user_itineraries(self):
        response = self.client.get(
            "/api/itineraries/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_retrieve_itinerary(self):
        response = self.client.get(
            f"/api/itineraries/{self.itinerary.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Cape Town Trip",
        )

    def test_update_itinerary(self):
        data = {
            "title": "Updated Cape Town Trip",
            "description": "Updated description",
            "start_date": "2026-10-01",
            "end_date": "2026-10-07",
            "status": "confirmed",
        }

        response = self.client.put(
            f"/api/itineraries/{self.itinerary.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.itinerary.refresh_from_db()

        self.assertEqual(
            self.itinerary.title,
            "Updated Cape Town Trip",
        )

    def test_delete_itinerary(self):
        response = self.client.delete(
            f"/api/itineraries/{self.itinerary.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(Itinerary.objects.filter(id=self.itinerary.id).exists())

    def test_other_user_cannot_modify_itinerary(self):
        self.client.force_authenticate(user=self.other_user)

        data = {
            "title": "Attempted Update",
            "description": "Should not be allowed",
            "start_date": "2026-10-01",
            "end_date": "2026-10-05",
            "status": "planning",
        }

        response = self.client.put(
            f"/api/itineraries/{self.itinerary.id}/",
            data,
            format="json",
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND,
            ],
        )
