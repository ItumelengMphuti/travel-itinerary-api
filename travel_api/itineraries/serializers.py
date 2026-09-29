from rest_framework import serializers

from .models import Itinerary


class ItinerarySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Itinerary
        fields = [
            "id",
            "user",
            "title",
            "description",
            "start_date",
            "end_date",
            "status",
            "destinations",
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
        if data["end_date"] < data["start_date"]:
            raise serializers.ValidationError(
                "End date cannot be before start date."
            )

        return data