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

    filterset_fields = [
        "status",
        "check_in",
        "check_out",
    ]

    search_fields = [
        "name",
        "location",
        "booking_reference",
    ]

    ordering_fields = [
        "name",
        "check_in",
        "check_out",
        "price",
        "created_at",
    ]

    ordering = ["check_in"]

    def get_queryset(self):
        return (
            AccommodationBooking.objects
            .select_related(
                "itinerary",
                "user",
            )
            .filter(user=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class ActivityBookingViewSet(viewsets.ModelViewSet):
    serializer_class = ActivityBookingSerializer

    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    filterset_fields = [
        "status",
        "activity_date",
    ]

    search_fields = [
        "name",
        "location",
        "booking_reference",
    ]

    ordering_fields = [
        "name",
        "activity_date",
        "price",
        "created_at",
    ]

    ordering = ["activity_date"]

    def get_queryset(self):
        return (
            ActivityBooking.objects
            .select_related(
                "itinerary",
                "user",
            )
            .filter(user=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )