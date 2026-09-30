from django.db import models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsOwnerOrReadOnly

from .models import Itinerary, ItineraryParticipant
from .serializers import (
    ItinerarySerializer,
    ItineraryParticipantSerializer,
)


class ItineraryViewSet(viewsets.ModelViewSet):
    serializer_class = ItinerarySerializer

    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        return Itinerary.objects.filter(
            models.Q(user=self.request.user)
            | models.Q(participants__user=self.request.user)
        ).prefetch_related(
            "destinations",
            "participants",
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class ItineraryParticipantViewSet(viewsets.ModelViewSet):
    serializer_class = ItineraryParticipantSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return ItineraryParticipant.objects.filter(
            itinerary__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )