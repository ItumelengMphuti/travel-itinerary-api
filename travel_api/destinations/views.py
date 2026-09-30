from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Destination
from .serializers import CategorySerializer, DestinationSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    filterset_fields = [
        "country",
        "city",
        "category",
        "is_active",
    ]

    search_fields = [
        "name",
        "country",
        "city",
        "description",
    ]

    ordering_fields = [
        "name",
        "country",
        "average_rating",
        "created_at",
    ]

    ordering = ["name"]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recommendations(request):
    user = request.user

    queryset = Destination.objects.filter(is_active=True)

    filters = Q()

    if user.preferred_destination:
        term = user.preferred_destination

        filters |= (
            Q(name__icontains=term)
            | Q(country__icontains=term)
            | Q(city__icontains=term)
        )

    if user.travel_style:
        filters |= Q(description__icontains=user.travel_style)

    if filters:
        queryset = queryset.filter(filters)

    queryset = queryset.order_by("-average_rating")[:5]

    serializer = DestinationSerializer(queryset, many=True)

    return Response(serializer.data)