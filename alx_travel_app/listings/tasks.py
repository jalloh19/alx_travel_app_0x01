from celery import shared_task
from django.core.mail import send_mail
from .models import Booking

@shared_task
def send_payment_confirmation_email(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        subject = 'Payment Confirmation'
        message = f'Dear {booking.guest.first_name},\n\nYour payment for booking {booking.id} has been successfully processed. Your booking is now confirmed.\n\nThank you for choosing ALX Travel App!'
        recipient_list = [booking.guest.email]
        send_mail(subject, message, 'noreply@alxtravelapp.com', recipient_list)
        return f"Email sent to {booking.guest.email}"
    except Booking.DoesNotExist:
        return "Booking not found"
    except Exception as e:
        return str(e)
