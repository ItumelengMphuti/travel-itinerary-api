from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsOwnerOrReadOnly

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        return Review.objects.select_related(
            "destination",
            "user",
        ).filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    filterset_fields = [
        "destination",
        "rating",
    ]


search_fields = [
    "comment",
    "destination__name",
]

ordering_fields = [
    "rating",
    "created_at",
    "updated_at",
]

ordering = ["-created_at"]
