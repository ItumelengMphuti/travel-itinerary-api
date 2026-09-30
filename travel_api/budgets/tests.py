from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from itineraries.models import Itinerary

from .models import Budget


User = get_user_model()


class BudgetAPITestCase(APITestCase):

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

    def test_create_budget(self):
        data = {
            "itinerary": self.itinerary.id,
            "total_budget": "10000.00",
            "accommodation_cost": "4000.00",
            "activity_cost": "2000.00",
            "transport_cost": "1000.00",
            "food_cost": "1500.00",
            "other_cost": "500.00",
        }

        response = self.client.post(
            "/api/budgets/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Budget.objects.count(),
            1,
        )

    def test_budget_rejects_expenses_above_total(self):
        data = {
            "itinerary": self.itinerary.id,
            "total_budget": "5000.00",
            "accommodation_cost": "4000.00",
            "activity_cost": "3000.00",
        }

        response = self.client.post(
            "/api/budgets/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_budget_rejects_negative_cost(self):
        data = {
            "itinerary": self.itinerary.id,
            "total_budget": "5000.00",
            "accommodation_cost": "-100.00",
        }

        response = self.client.post(
            "/api/budgets/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_list_budgets(self):
        Budget.objects.create(
            itinerary=self.itinerary,
            user=self.user,
            total_budget="10000.00",
            accommodation_cost="4000.00",
            activity_cost="2000.00",
            transport_cost="1000.00",
            food_cost="1500.00",
            other_cost="500.00",
        )

        response = self.client.get(
            "/api/budgets/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )