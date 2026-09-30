from rest_framework.routers import DefaultRouter

from .views import BudgetViewSet, TripExpenseViewSet

router = DefaultRouter()

router.register(
    "budgets",
    BudgetViewSet,
    basename="budget",
)

router.register(
    "expenses",
    TripExpenseViewSet,
    basename="expense",
)

urlpatterns = router.urls
