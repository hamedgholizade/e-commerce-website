from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

@shared_task
def send_otp_email(code, email):
    subject = 'Your OTP Code'
    message = f'Your verification code is: {code}'
    recipient = [email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient)
