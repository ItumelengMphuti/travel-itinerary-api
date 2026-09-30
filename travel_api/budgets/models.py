from django.conf import settings
from django.db import models


class Budget(models.Model):
    itinerary = models.OneToOneField(
        "itineraries.Itinerary",
        on_delete=models.CASCADE,
        related_name="budget",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="budgets",
    )

    total_budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    accommodation_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    activity_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    transport_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    food_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    other_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.itinerary.title} Budget"