from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Destination

User = get_user_model()


class DestinationAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123",
        )

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name="Nature",
        )

        self.destination = Destination.objects.create(
            name="Cape Town",
            country="South Africa",
            city="Cape Town",
            description="A beautiful coastal city.",
            category=self.category,
            is_active=True,
        )

    def test_list_destinations(self):
        response = self.client.get("/api/destinations/destinations/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_retrieve_destination(self):
        response = self.client.get(
            f"/api/destinations/destinations/{self.destination.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["name"],
            "Cape Town",
        )

    def test_create_destination(self):
        data = {
            "name": "Kruger National Park",
            "country": "South Africa",
            "city": "Mbombela",
            "description": "A famous wildlife destination.",
            "category_id": self.category.id,
            "is_active": True,
        }

        response = self.client.post(
            "/api/destinations/destinations/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Destination.objects.count(),
            2,
        )

    def test_search_destinations(self):
        response = self.client.get("/api/destinations/destinations/?search=Cape")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertGreaterEqual(
            response.data["count"],
            1,
        )

    def test_filter_destinations_by_country(self):
        response = self.client.get(
            "/api/destinations/destinations/?country=South%20Africa"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_unauthenticated_user_cannot_access_destinations(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/destinations/destinations/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
