from rest_framework.routers import DefaultRouter

from .views import (
    ItineraryViewSet,
    ItineraryParticipantViewSet,
)


router = DefaultRouter()

router.register(
    "itineraries",
    ItineraryViewSet,
    basename="itinerary",
)

router.register(
    "participants",
    ItineraryParticipantViewSet,
    basename="itinerary-participant",
)


urlpatterns = router.urls