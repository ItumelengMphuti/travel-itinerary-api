from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .models import Category, Destination
from .serializers import CategorySerializer, DestinationSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = ["country", "city", "category", "is_active"]
    search_fields = ["name", "country", "city", "description"]
    ordering_fields = ["name", "country", "average_rating", "created_at"]
    ordering = ["name"]