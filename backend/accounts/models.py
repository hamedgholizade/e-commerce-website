from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager

from base.models import BaseModelQuerySet, BaseModel


class UserManager(DjangoUserManager.from_queryset(BaseModelQuerySet)):
    """
    Custom UserManager that extends Django's UserManager with additional queryset methods.
    """
    pass


class User(AbstractUser, BaseModel):
    """
    Custom User model that extends Django's AbstractUser.
    """
    USER_ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='customer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email
