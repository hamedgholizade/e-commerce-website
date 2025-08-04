from django.contrib.auth.models import UserManager as DjangoUserManager

from base.models import BaseModelQuerySet


class UserManager(DjangoUserManager.from_queryset(BaseModelQuerySet)):
    """
    Custom UserManager that supports 'phone' as the USERNAME_FIELD
    """
    def create_user(self, phone, email=None, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")
        if not password:
            raise ValueError('Password is required')
        if email:
            email = self.normalize_email(email)
        extra_fields.setdefault('username', phone)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone=phone, email=email, password=password, **extra_fields)
