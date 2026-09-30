from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class BookingStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"


class AccommodationBooking(models.Model):
    itinerary = models.ForeignKey(
        "itineraries.Itinerary",
        on_delete=models.CASCADE,
        related_name="accommodation_bookings",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accommodation_bookings",
    )
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    check_in = models.DateField()
    check_out = models.DateField()
    booking_reference = models.CharField(
        max_length=100,
        blank=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["check_in"]
        indexes = [
            models.Index(fields=["itinerary"]),
            models.Index(fields=["user"]),
            models.Index(fields=["check_in"]),
        ]

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("Check-out date must be after check-in date.")

        if self.price < 0:
            raise ValidationError("Price cannot be negative.")

    def __str__(self):
        return self.name


class ActivityBooking(models.Model):
    itinerary = models.ForeignKey(
        "itineraries.Itinerary",
        on_delete=models.CASCADE,
        related_name="activity_bookings",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activity_bookings",
    )
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    activity_date = models.DateField()
    booking_reference = models.CharField(
        max_length=100,
        blank=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["activity_date"]
        indexes = [
            models.Index(fields=["itinerary"]),
            models.Index(fields=["user"]),
            models.Index(fields=["activity_date"]),
        ]

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")

    def __str__(self):
        return self.name
