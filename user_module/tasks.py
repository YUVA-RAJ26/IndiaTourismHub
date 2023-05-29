from celery import shared_task
from django.core.mail import send_mail
from user_module.models import Booking

@shared_task
def send_payment_reminder_emails():
    # Fetch bookings with incomplete payments
    bookings = Booking.objects.filter(payment_rejected=False, payment_approved=False)

    # Iterate over the bookings and send reminder emails
    for booking in bookings:
        # Send email using Django's send_mail function
        from_email = 'yuvaraj@spericorn.com'
        send_mail(
            'Payment Reminder',
            'Please complete your payment for booking ID {}'.format(booking.id),
            from_email,
            [booking.user.email],
            fail_silently=False,
        )

@shared_task
def send_otp_email_task(email, otp):
    # Send OTP email
    subject = 'OTP Verification'
    message = f'Your OTP is: {otp}'
    from_email = 'yuvaraj@spericorn.com'  # Replace with your email address
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

    return otp