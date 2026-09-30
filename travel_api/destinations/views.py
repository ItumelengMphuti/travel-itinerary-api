from django.db.models import Avg, Count, Q

from reviews.models import Review

from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Destination
from .serializers import CategorySerializer, DestinationSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.select_related("category").all()
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

    @action(detail=True, methods=["get"])
    def reviews(self, request, pk=None):
        """
        Return reviews for a destination.

        Example:
            GET /api/v1/destinations/{id}/reviews/
        """
        destination = self.get_object()

        reviews = Review.objects.filter(destination=destination).select_related("user")

        data = [
            {
                "id": review.id,
                "username": review.user.username,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at,
            }
            for review in reviews
        ]

        return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recommendations(request):
    """
    Return destination recommendations based on the authenticated user's
    preferred destination and travel style.

    Example:
        GET /api/v1/destinations/recommendations/
    """
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def popular_destinations(request):
    """
    Return the 10 highest-rated active destinations.

    Example:
        GET /api/v1/destinations/popular/
    """

    destinations = Destination.objects.filter(is_active=True).order_by(
        "-average_rating"
    )[:10]

    serializer = DestinationSerializer(destinations, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def destination_statistics(request):
    """
    Return statistics for active destinations.

    Example:
        GET /api/v1/destinations/statistics/
    """

    statistics = Destination.objects.filter(is_active=True).aggregate(
        total_destinations=Count("id"),
        average_rating=Avg("average_rating"),
    )

    return Response(
        {
            "total_destinations": statistics["total_destinations"],
            "average_rating": statistics["average_rating"] or 0,
        }
    )
