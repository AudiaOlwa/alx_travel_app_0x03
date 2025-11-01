from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

@shared_task
def send_booking_confirmation(email, booking_id):
    subject = "Booking Confirmation"
    message = f"Your booking #{booking_id} has been confirmed!"
    send_mail(subject, message, "noreply@travelapp.com", [email])


@shared_task
def send_booking_email(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        user = booking.user
        listing = booking.listing

        subject = "Booking Confirmation"
        message = f"""
        Hello {user.username},

        Your booking for '{listing.title}' from {booking.start_date} to {booking.end_date} has been confirmed.

        Thank you for using our platform!
        """
        
        recipient_email = user.email  # Ensure user has an email set

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient_email],
            fail_silently=False,
        )

        return f"Email sent to {recipient_email} for booking ID {booking_id}"

    except Exception as e:
        return f"Error sending email: {str(e)}"
