from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from destinations.models import Category, Destination

from .models import Review

User = get_user_model()


class ReviewAPITestCase(APITestCase):

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

    def test_create_review(self):
        data = {
            "destination": self.destination.id,
            "rating": 5,
            "comment": "Amazing destination!",
        }

        response = self.client.post(
            "/api/reviews/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Review.objects.count(),
            1,
        )

    def test_review_rejects_rating_above_five(self):
        data = {
            "destination": self.destination.id,
            "rating": 6,
            "comment": "Invalid rating.",
        }

        response = self.client.post(
            "/api/reviews/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_review_rejects_rating_below_one(self):
        data = {
            "destination": self.destination.id,
            "rating": 0,
            "comment": "Invalid rating.",
        }

        response = self.client.post(
            "/api/reviews/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_list_reviews(self):
        Review.objects.create(
            destination=self.destination,
            user=self.user,
            rating=5,
            comment="Excellent!",
        )

        response = self.client.get("/api/reviews/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_unauthenticated_user_cannot_create_review(self):
        self.client.force_authenticate(user=None)

        data = {
            "destination": self.destination.id,
            "rating": 5,
            "comment": "Should not be created.",
        }

        response = self.client.post(
            "/api/reviews/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
