from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsOwnerOrReadOnly

from .models import Budget, TripExpense
from .serializers import BudgetSerializer, TripExpenseSerializer


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        return (
            Budget.objects.select_related(
                "itinerary",
                "user",
            )
            .prefetch_related("expenses")
            .filter(user=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        """Return a summary of the itinerary budget."""

        budget = self.get_object()

        total_expenses = (
            budget.accommodation_cost
            + budget.activity_cost
            + budget.transport_cost
            + budget.food_cost
            + budget.other_cost
        )

        remaining = budget.total_budget - total_expenses

        return Response(
            {
                "total_budget": budget.total_budget,
                "total_expenses": total_expenses,
                "remaining": remaining,
            }
        )


class TripExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = TripExpenseSerializer

    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    filterset_fields = [
        "budget",
        "category",
        "expense_date",
    ]

    search_fields = [
        "description",
    ]

    ordering_fields = [
        "amount",
        "expense_date",
    ]

    ordering = ["-expense_date"]

    def get_queryset(self):
        return TripExpense.objects.select_related(
            "budget",
            "user",
        ).filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
