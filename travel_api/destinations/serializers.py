from rest_framework import serializers

from .models import Category, Destination


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class DestinationSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
    )

    class Meta:
        model = Destination
        fields = [
            "id",
            "name",
            "country",
            "city",
            "description",
            "category",
            "category_id",
            "image",
            "average_rating",
            "is_active",
            "created_at",
            "uploaded_at",
        ]
        read_only_fields = [
            "id",
            "category",
            "average_rating",
            "created_at",
            "uploaded_at",
        ]
