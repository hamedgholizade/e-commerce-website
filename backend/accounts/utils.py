from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

def send_custom_email(subject, message, recipient_list):
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)


def custom_normalize_email(email: str) -> str | None:
    """
    Normalize the emil address with lower case domain to format (e.g., example@example.com).
    Returns th email address string, or None if normalization fails.
    """
    if not email or email.count('@') != 1:
        return None
    local, domain = email.rsplit('@', 1)
    if not local or not domain:
        return None
    return f"{local}@{domain.lower()}"


def custom_validate_email(email: str) -> bool:
    """
    validation of Email address.
    if it's valid return True else return False.
    """
    try:
        django_validate_email(email.strip())
        return True
    except DjangoValidationError:
        return False

def custom_normalize_phone(phone: str) -> str | None :
    """
    Normalize the phone number with region 'IR' to format (e.g., 9123456789).
    Returns the phone number string, or None if parsing fails.
    """
    if not phone:
        return None
    try:
        parsed = phonenumbers.parse(phone, "IR")
        phone = str(parsed.national_number)
        if phone.startswith('98'):
            return phone[2:]
        return phone
    except NumberParseException:
        return None

def custom_validate_phone(phone: str) -> bool:
    """
    validation of phone number with region IR.
    if it's valid return True else return False.
    """
    try:
        parsed = phonenumbers.parse(phone, "IR")
        return phonenumbers.is_valid_number(parsed)
    except NumberParseException:
        return False
