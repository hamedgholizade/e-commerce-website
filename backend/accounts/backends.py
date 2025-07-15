from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class PhoneEmailUsernameAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in
    using either their username or phone number or email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            # Try to find the user by username and phone number and email
            user = User.objects.get(
                Q(username=username) | Q(phone=username) | Q(email=username)
            )
        except User.DoesNotExist:
            # If not found, return None
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
