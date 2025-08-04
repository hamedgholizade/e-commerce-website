from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task
def send_order_status_email(status, email):
    subject = 'Changing Order status'
    message = f'your order status is change to {status}'
    recipient = [email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient)
