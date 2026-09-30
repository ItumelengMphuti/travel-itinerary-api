from django.conf import settings
from django.core.exceptions import ValidationError
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

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["created_at"]),
        ]

    def clean(self):
        costs = [
            self.accommodation_cost,
            self.activity_cost,
            self.transport_cost,
            self.food_cost,
            self.other_cost,
        ]

        if self.total_budget < 0:
            raise ValidationError("Total budget cannot be negative.")

        if any(cost < 0 for cost in costs):
            raise ValidationError("Budget costs cannot be negative.")

        if sum(costs) > self.total_budget:
            raise ValidationError("Total expenses cannot exceed the total budget.")

    def __str__(self):
        return f"{self.itinerary.title} Budget"


class TripExpense(models.Model):
    class ExpenseCategory(models.TextChoices):
        ACCOMMODATION = "accommodation", "Accommodation"
        ACTIVITY = "activity", "Activity"
        TRANSPORT = "transport", "Transport"
        FOOD = "food", "Food"
        OTHER = "other", "Other"

    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name="expenses",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trip_expenses",
    )
    description = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=ExpenseCategory.choices,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    expense_date = models.DateField()

    class Meta:
        ordering = ["-expense_date"]
        indexes = [
            models.Index(fields=["budget"]),
            models.Index(fields=["category"]),
            models.Index(fields=["expense_date"]),
        ]

    def clean(self):
        if self.amount < 0:
            raise ValidationError("Expense amount cannot be negative.")

    def __str__(self):
        return f"{self.description} - {self.amount}"
