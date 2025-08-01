from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

@shared_task
def send_custom_email(subject, message, recipient_list):
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    