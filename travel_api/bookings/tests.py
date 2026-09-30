from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from itineraries.models import Itinerary

from .models import AccommodationBooking, ActivityBooking


User = get_user_model()


class BookingAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
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

    def test_create_accommodation_booking(self):
        data = {
            "itinerary": self.itinerary.id,
            "name": "Cape Town Hotel",
            "location": "Cape Town",
            "check_in": "2026-10-01",
            "check_out": "2026-10-05",
            "booking_reference": "HOTEL123",
            "price": "5000.00",
        }

        response = self.client.post(
            "/api/accommodations/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            AccommodationBooking.objects.count(),
            1,
        )

    def test_accommodation_booking_rejects_invalid_dates(self):
        data = {
            "itinerary": self.itinerary.id,
            "name": "Cape Town Hotel",
            "location": "Cape Town",
            "check_in": "2026-10-05",
            "check_out": "2026-10-01",
            "booking_reference": "HOTEL123",
            "price": "5000.00",
        }

        response = self.client.post(
            "/api/accommodations/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_list_accommodation_bookings(self):
        AccommodationBooking.objects.create(
            itinerary=self.itinerary,
            user=self.user,
            name="Cape Town Hotel",
            location="Cape Town",
            check_in="2026-10-01",
            check_out="2026-10-05",
            price="5000.00",
        )

        response = self.client.get(
            "/api/accommodations/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_create_activity_booking(self):
        data = {
            "itinerary": self.itinerary.id,
            "name": "Table Mountain Hike",
            "location": "Cape Town",
            "activity_date": "2026-10-03",
            "booking_reference": "ACT123",
            "price": "800.00",
        }

        response = self.client.post(
            "/api/activities/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            ActivityBooking.objects.count(),
            1,
        )

    def test_list_activity_bookings(self):
        ActivityBooking.objects.create(
            itinerary=self.itinerary,
            user=self.user,
            name="Table Mountain Hike",
            location="Cape Town",
            activity_date="2026-10-03",
            price="800.00",
        )

        response = self.client.get(
            "/api/activities/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_unauthenticated_user_cannot_create_booking(self):
        self.client.force_authenticate(user=None)

        data = {
            "itinerary": self.itinerary.id,
            "name": "Cape Town Hotel",
            "location": "Cape Town",
            "check_in": "2026-10-01",
            "check_out": "2026-10-05",
            "price": "5000.00",
        }

        response = self.client.post(
            "/api/accommodations/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )