from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Itinerary(models.Model):
    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="itineraries",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(
        upload_to="itineraries/",
        blank=True,
        null=True,
    )

    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
    )

    destinations = models.ManyToManyField(
        "destinations.Destination",
        related_name="itineraries",
        blank=True,
    )

    participants_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ItineraryParticipant",
        related_name="collaborative_itineraries",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_date"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["start_date"]),
            models.Index(fields=["status"]),
        ]

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")

    def __str__(self):
        return self.title


class ItineraryParticipant(models.Model):
    class Role(models.TextChoices):
        EDITOR = "editor", "Editor"
        VIEWER = "viewer", "Viewer"

    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        related_name="participants",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shared_itineraries",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-joined_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["itinerary", "user"],
                name="unique_itinerary_participant",
            )
        ]
        indexes = [
            models.Index(fields=["itinerary", "user"]),
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.itinerary.title}"
