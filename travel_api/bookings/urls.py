from rest_framework.routers import DefaultRouter

from .views import (
    AccommodationBookingViewSet,
    ActivityBookingViewSet,
)

router = DefaultRouter()

router.register(
    "accommodations",
    AccommodationBookingViewSet,
    basename="accommodation-booking",
)

router.register(
    "activities",
    ActivityBookingViewSet,
    basename="activity-booking",
)

urlpatterns = router.urls
