from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    DestinationViewSet,
    recommendations,
)

router = DefaultRouter()

router.register("categories", CategoryViewSet, basename="category")
router.register("destinations", DestinationViewSet, basename="destination")

urlpatterns = [
    path("recommendations/", recommendations, name="recommendations"),
] + router.urls