from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsOwnerOrReadOnly

from .models import AccommodationBooking, ActivityBooking
from .serializers import (
    AccommodationBookingSerializer,
    ActivityBookingSerializer,
)


class AccommodationBookingViewSet(viewsets.ModelViewSet):
    serializer_class = AccommodationBookingSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        return AccommodationBooking.objects.select_related(
        "itinerary",
        "user",
        ).filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActivityBookingViewSet(viewsets.ModelViewSet):
    serializer_class = ActivityBookingSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        return ActivityBooking.objects.select_related(
        "itinerary",
        "user",
    ).filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)