from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
import io 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_invoice_email(booking, invoice_pdf):
    # Render email template with booking details
    email_subject = 'Invoice for Booking'
    email_body = 'Hi! Happy travelling Please find the invoice! Make a payment and update to confrom booking'
    to = [booking.user.email]

    # Create the email message
    email_message = EmailMessage(
        email_subject,
        email_body,
        to=to,
    )
    
    # Attach the invoice PDF to the email
    email_message.attach('invoice.pdf', invoice_pdf.getvalue(), 'application/pdf')

    #email_message.send()

    # Send the email
    try:
        email_message.send()
    except Exception as e:
        return True
    return True

def generate_invoice_pdf(booking):
    buffer = io.BytesIO()

    # Create the PDF object
    p = canvas.Canvas(buffer)

    # Customize and draw the invoice contents
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, "Invoice for Booking ID: {}".format(booking.id))
    p.drawString(50, 700, "Customer Name: {}".format(booking.user.username))
    p.drawString(50, 650, "Tour Package: {}".format(booking.tour_package.name))
    p.drawString(50, 600, "Booking Date: {}".format(booking.book_date.strftime("%Y-%m-%d")))
    p.drawString(50, 550, "Contact Number: {}".format(booking.contact_number))
    p.drawString(50, 450, "Number of Adults: {}".format(booking.num_adults))
    p.drawString(50, 400, "Number of Children: {}".format(booking.num_children))
    p.drawString(50, 350, "Price: ${}".format(booking.price))

    # Save the PDF
    p.showPage()
    p.save()

    # Set the buffer position to the beginning
    buffer.seek(0)

    return buffer

def send_booking_approved_email(booking):
    subject = 'Booking Approved'
    html_message = render_to_string('booking/booking_approved.html', {'booking': booking})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = booking.user.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)