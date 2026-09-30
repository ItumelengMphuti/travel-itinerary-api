from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    DestinationViewSet,
    recommendations,
    popular_destinations,
    destination_statistics,
)

router = DefaultRouter()

router.register("categories", CategoryViewSet, basename="category")
router.register("destinations", DestinationViewSet, basename="destination")

urlpatterns = [
    path("recommendations/", recommendations, name="recommendations"),
    path("popular/", popular_destinations, name="popular-destinations"),
    path("statistics/", destination_statistics, name="destination-statistics"),
] + router.urls