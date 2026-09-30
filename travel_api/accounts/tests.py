from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AccountAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123",
        )

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "NewPassword123",
            "travel_style": "Adventure",
            "preferred_destination": "Cape Town",
            "budget_preference": "10000.00",
        }

        response = self.client.post(
            "/api/auth/register/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                username="newuser"
            ).exists()
        )

    def test_registration_requires_password(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
        }

        response = self.client.post(
            "/api/auth/register/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_registration_rejects_short_password(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "short",
        }

        response = self.client.post(
            "/api/auth/register/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_jwt_login(self):
        data = {
            "username": "testuser",
            "password": "TestPassword123",
        }

        response = self.client.post(
            "/api/auth/token/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_jwt_login_rejects_wrong_password(self):
        data = {
            "username": "testuser",
            "password": "WrongPassword123",
        }

        response = self.client.post(
            "/api/auth/token/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_jwt_refresh(self):
        login_data = {
            "username": "testuser",
            "password": "TestPassword123",
        }

        login_response = self.client.post(
            "/api/auth/token/",
            login_data,
            format="json",
        )

        refresh_token = login_response.data["refresh"]

        response = self.client.post(
            "/api/auth/token/refresh/",
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)