from django.db import models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from accounts.permissions import IsOwnerOrReadOnly

from .models import Itinerary, ItineraryParticipant
from .serializers import (
    ItinerarySerializer,
    ItineraryParticipantSerializer,
)


class ItineraryViewSet(viewsets.ModelViewSet):
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    filterset_fields = [
        "status",
        "start_date",
        "end_date",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "title",
        "start_date",
        "end_date",
        "created_at",
        "status",
    ]

    ordering = ["start_date"]

    def get_queryset(self):
        return (
            Itinerary.objects.filter(
                models.Q(user=self.request.user)
                | models.Q(participants__user=self.request.user)
            )
            .prefetch_related(
                "destinations",
                "participants",
            )
            .distinct()
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"])
    def share(self, request, pk=None):
        """Return basic information that can be shared about an itinerary."""
        itinerary = self.get_object()

        return Response(
            {
                "id": itinerary.id,
                "title": itinerary.title,
                "description": itinerary.description,
                "start_date": itinerary.start_date,
                "end_date": itinerary.end_date,
                "status": itinerary.status,
            }
        )

    @action(detail=True, methods=["get"])
    def participants(self, request, pk=None):
        """Return the users participating in an itinerary."""
        itinerary = self.get_object()

        participants = itinerary.participants.select_related("user").all()

        data = [
            {
                "username": participant.user.username,
                "role": participant.role,
                "joined_at": participant.joined_at,
            }
            for participant in participants
        ]

        return Response(data)

    @action(
        detail=True,
        methods=["post"],
        parser_classes=[MultiPartParser, FormParser],
    )
    def upload_cover(self, request, pk=None):
        """Upload a cover image for an itinerary."""
        itinerary = self.get_object()

        image = request.FILES.get("cover_image")

        if not image:
            return Response(
                {"error": "No cover image was provided."},
                status=400,
            )

        itinerary.cover_image = image
        itinerary.save(update_fields=["cover_image"])

        return Response(
            {
                "message": "Cover image uploaded successfully.",
                "cover_image": itinerary.cover_image.url,
            }
        )


class ItineraryParticipantViewSet(viewsets.ModelViewSet):
    serializer_class = ItineraryParticipantSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return ItineraryParticipant.objects.filter(itinerary__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
