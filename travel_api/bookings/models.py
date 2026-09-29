from django.conf import settings
from django.db import models


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

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

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

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name