from django.db import models
from django.contrib.auth.models import AbstractUser

from base.models import BaseModel
from accounts.managers import UserManager


class User(AbstractUser, BaseModel):
    """
    Custom User model that extends Django's AbstractUser.
    """
    
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    picture = models.ImageField(
        upload_to='accounts/profile_pictures/', default='accounts/profile_pictures/default.jpg'
    )
    is_seller = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return f"{self.email} ({self.phone})"
