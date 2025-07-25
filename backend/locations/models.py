from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from base.models import BaseModel
from stores.models import Store

User = get_user_model()


class Address(BaseModel):
    """
    Model representing addresses of users and stores.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        null=True,
        blank=True
    )
    store = models.OneToOneField(
        Store,
        on_delete=models.CASCADE,
        related_name='address',
        null=True,
        blank=True
    )
    label = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20)
    
    def clean(self):
        if not self.user and not self.store:
            raise ValidationError("At least one of user or store must be set.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation is run before saving
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"
    