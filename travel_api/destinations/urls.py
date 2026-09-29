from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, DestinationViewSet


router = DefaultRouter()

router.register("categories", CategoryViewSet)
router.register("destinations", DestinationViewSet)

urlpatterns = router.urls