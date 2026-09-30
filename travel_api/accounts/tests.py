from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from itineraries.models import Itinerary, ItineraryParticipant

from .permissions import (
    IsOwnerOrReadOnly,
    IsItineraryOwner,
    IsItineraryParticipant,
    IsOwnerOrParticipant,
)

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
        
class PermissionTests(TestCase):

    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="owner",
            password="password123",
        )

        self.participant = get_user_model().objects.create_user(
            username="participant",
            password="password123",
        )

        self.other_user = get_user_model().objects.create_user(
            username="other",
            password="password123",
        )

        self.itinerary = Itinerary.objects.create(
            user=self.owner,
            title="Cape Town Trip",
            description="A test trip",
            start_date="2026-10-01",
            end_date="2026-10-05",
        )

        ItineraryParticipant.objects.create(
            itinerary=self.itinerary,
            user=self.participant,
            role="viewer",
        )

        self.factory = APIRequestFactory()

    def test_owner_or_read_only_allows_owner_to_modify(self):
        request = self.factory.patch("/")
        request.user = self.owner

        permission = IsOwnerOrReadOnly()

        self.assertTrue(
            permission.has_object_permission(
                request,
                None,
                self.itinerary,
            )
        )

    def test_owner_or_read_only_blocks_other_user_from_modify(self):
        request = self.factory.patch("/")
        request.user = self.other_user

        permission = IsOwnerOrReadOnly()

        self.assertFalse(
            permission.has_object_permission(
                request,
                None,
                self.itinerary,
            )
        )

    def test_itinerary_owner_allows_owner(self):
        request = self.factory.get("/")
        request.user = self.owner

        permission = IsItineraryOwner()

        self.assertTrue(
            permission.has_object_permission(
                request,
                None,
                self.itinerary,
            )
        )

    def test_itinerary_owner_blocks_other_user(self):
        request = self.factory.get("/")
        request.user = self.other_user

        permission = IsItineraryOwner()

        self.assertFalse(
            permission.has_object_permission(
                request,
                None,
                self.itinerary,
            )
        )

    def test_participant_permission_allows_participant(self):
        request = self.factory.get("/")
        request.user = self.participant

        permission = IsItineraryParticipant()

        self.assertTrue(
            permission.has_object_permission(
                request,
                None,
                self.itinerary,
            )
        )

    def test_participant_permission_blocks_other_user(self):
        request = self.factory.get("/")
        request.user = self.other_user

        permission = IsItineraryParticipant()

        self.assertFalse(
            permission.has_object_permission(
                request,
                None,
                self.itinerary,
            )
        )

    def test_owner_or_participant_allows_owner(self):
        request = self.factory.get("/")
        request.user = self.owner

        permission = IsOwnerOrParticipant()

        self.assertTrue(
            permission.has_object_permission(
                request,
                None,
                self.itinerary,
            )
        )

    def test_owner_or_participant_allows_participant(self):
        request = self.factory.get("/")
        request.user = self.participant

        permission = IsOwnerOrParticipant()

        self.assertTrue(
            permission.has_object_permission(
                request,
                None,
                self.itinerary,
            )
        )

    def test_owner_or_participant_blocks_other_user(self):
        request = self.factory.get("/")
        request.user = self.other_user

        permission = IsOwnerOrParticipant()

        self.assertFalse(
            permission.has_object_permission(
                request,
                None,
                self.itinerary,
            )
        )