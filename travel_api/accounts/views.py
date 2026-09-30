from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    PasswordChangeSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user account.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveAPIView):
    """
    Retrieve the authenticated user's profile.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(generics.UpdateAPIView):
    """
    Update the authenticated user's profile.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordChangeView(generics.UpdateAPIView):
    """
    Change the authenticated user's password.
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
