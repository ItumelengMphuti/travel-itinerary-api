from rest_framework import serializers

from .models import AccommodationBooking, ActivityBooking


class AccommodationBookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = AccommodationBooking

        fields = [
            "id",
            "itinerary",
            "user",
            "name",
            "location",
            "check_in",
            "check_out",
            "booking_reference",
            "price",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )

        return data


class ActivityBookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = ActivityBooking

        fields = [
            "id",
            "itinerary",
            "user",
            "name",
            "location",
            "activity_date",
            "booking_reference",
            "price",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]