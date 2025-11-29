"""Routes exposed by the listings application."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, HealthCheckView, ListingViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="listings-health"),
    path("", include(router.urls)),
]
