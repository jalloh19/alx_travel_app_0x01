"""API endpoints for listings-related functionality."""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Listing
from .serializers import BookingSerializer, ListingSerializer


class HealthCheckView(APIView):
    """Simple endpoint to verify that the service is responding."""

    def get(self, request):
        return Response({"status": "ok"})


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Listing resources.
    
    Provides full CRUD operations:
    - list: GET /api/listings/
    - create: POST /api/listings/
    - retrieve: GET /api/listings/{id}/
    - update: PUT /api/listings/{id}/
    - partial_update: PATCH /api/listings/{id}/
    - destroy: DELETE /api/listings/{id}/
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    
    def get_queryset(self):
        """
        Optionally filter listings by query parameters.
        """
        queryset = Listing.objects.all()
        
        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by availability
        available = self.request.query_params.get('available', None)
        if available is not None:
            queryset = queryset.filter(available=available.lower() == 'true')
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        
        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Booking resources.
    
    Provides full CRUD operations:
    - list: GET /api/bookings/
    - create: POST /api/bookings/
    - retrieve: GET /api/bookings/{id}/
    - update: PUT /api/bookings/{id}/
    - partial_update: PATCH /api/bookings/{id}/
    - destroy: DELETE /api/bookings/{id}/
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        """
        Optionally filter bookings by query parameters.
        """
        queryset = Booking.objects.all()
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by guest
        guest_id = self.request.query_params.get('guest_id', None)
        if guest_id:
            queryset = queryset.filter(guest_id=guest_id)
        
        # Filter by listing
        listing_id = self.request.query_params.get('listing_id', None)
        if listing_id:
            queryset = queryset.filter(listing_id=listing_id)
        
        return queryset
