from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class PhoneEmailAuthBackkend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using either their phone number or email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        try:
            # Try to find the user by phone number first
            user = User.objects.get(Q(phone=username) | Q(email=username))
        except User.DoesNotExist:
            # If not found, return None
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
