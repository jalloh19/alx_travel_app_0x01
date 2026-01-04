"""API endpoints for listings-related functionality."""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import uuid
from django.conf import settings

from .models import Booking, Listing, Payment
from .serializers import BookingSerializer, ListingSerializer, PaymentSerializer


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


class InitiatePaymentView(APIView):
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a unique transaction ID
        tx_ref = str(uuid.uuid4())
        
        # Prepare payload for Chapa
        payload = {
            "amount": str(booking.total_price),
            "currency": "ETB",
            "email": booking.guest.email,
            "first_name": booking.guest.first_name,
            "last_name": booking.guest.last_name,
            "tx_ref": tx_ref,
            "callback_url": f"http://localhost:8000/api/payments/verify/{tx_ref}/",
            "return_url": f"http://localhost:8000/payment-success/",
            "customization[title]": "Booking Payment",
            "customization[description]": f"Payment for booking {booking.id}"
        }
        
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(settings.CHAPA_API_URL, json=payload, headers=headers)
            data = response.json()
            
            if data["status"] == "success":
                # Create Payment record
                Payment.objects.create(
                    booking=booking,
                    transaction_id=tx_ref,
                    amount=booking.total_price,
                    status="Pending"
                )
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    def get(self, request, tx_ref):
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
            
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
        }
        
        try:
            url = f"{settings.CHAPA_VERIFY_URL}/{tx_ref}"
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data["status"] == "success":
                payment.status = "Completed"
                payment.save()
                
                # Update booking status
                payment.booking.status = "confirmed"
                payment.booking.save()
                
                # Send confirmation email (Celery task)
                from .tasks import send_payment_confirmation_email
                send_payment_confirmation_email.delay(payment.booking.id)
                
                return Response({"status": "Payment verified successfully", "data": data}, status=status.HTTP_200_OK)
            else:
                payment.status = "Failed"
                payment.save()
                return Response({"status": "Payment verification failed", "data": data}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
