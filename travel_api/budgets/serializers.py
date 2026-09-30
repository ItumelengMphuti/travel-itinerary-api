from rest_framework import serializers

from .models import Budget, TripExpense


class BudgetSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Budget

        fields = [
            "id",
            "itinerary",
            "user",
            "total_budget",
            "accommodation_cost",
            "activity_cost",
            "transport_cost",
            "food_cost",
            "other_cost",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        total_budget = data.get("total_budget", 0)

        costs = [
            data.get("accommodation_cost", 0),
            data.get("activity_cost", 0),
            data.get("transport_cost", 0),
            data.get("food_cost", 0),
            data.get("other_cost", 0),
        ]

        if any(cost < 0 for cost in costs):
            raise serializers.ValidationError("Budget costs cannot be negative.")

        if total_budget < 0:
            raise serializers.ValidationError("Total budget cannot be negative.")

        if sum(costs) > total_budget:
            raise serializers.ValidationError(
                "Total expenses cannot exceed the total budget."
            )

        return data


class TripExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripExpense
        fields = [
            "id",
            "budget",
            "user",
            "description",
            "category",
            "amount",
            "expense_date",
        ]
        read_only_fields = [
            "id",
            "user",
        ]

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Expense amount cannot be negative.")

        return value
