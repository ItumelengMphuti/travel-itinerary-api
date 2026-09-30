from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Password must contain at least 8 characters.",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "travel_style",
            "preferred_destination",
            "budget_preference",
        ]
        extra_kwargs = {
            "username": {
                "help_text": "Unique username for the account."
            },
            "email": {
                "help_text": "User's email address."
            },
            "travel_style": {
                "help_text": "Preferred travel style, such as adventure or relaxation."
            },
            "preferred_destination": {
                "help_text": "Destination the user is interested in visiting."
            },
            "budget_preference": {
                "help_text": "Preferred travel budget."
            },
        }

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "travel_style",
            "preferred_destination",
            "budget_preference",
        ]
        read_only_fields = ["id", "username"]


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        help_text="Your current account password.",
    )

    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Your new password must contain at least 8 characters.",
    )

    def validate_old_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                "Current password is incorrect."
            )

        return value

    def save(self):
        user = self.context["request"].user

        user.set_password(
            self.validated_data["new_password"]
        )

        user.save()

        return user