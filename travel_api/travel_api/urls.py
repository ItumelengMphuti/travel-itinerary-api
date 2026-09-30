from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    # API documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),

    # Authentication
    path("api/auth/", include("accounts.urls")),

    # JWT
    path(
        "api/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # API v1
    path("api/v1/destinations/", include("destinations.urls")),
    path("api/v1/", include("itineraries.urls")),
    path("api/v1/", include("bookings.urls")),
    path("api/v1/", include("budgets.urls")),
    path("api/v1/", include("reviews.urls")),

    # Backwards-compatible API routes
    path("api/destinations/", include("destinations.urls")),
    path("api/", include("itineraries.urls")),
    path("api/", include("bookings.urls")),
    path("api/", include("budgets.urls")),
    path("api/", include("reviews.urls")),
]