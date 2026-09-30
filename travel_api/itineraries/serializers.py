from rest_framework import serializers

from .models import Itinerary, ItineraryParticipant


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
    
class ItineraryParticipantSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ItineraryParticipant
        fields = [
            "id",
            "itinerary",
            "user",
            "user_id",
            "joined_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "joined_at",
        ]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")

        return ItineraryParticipant.objects.create(
            user_id=user_id,
            **validated_data
        )