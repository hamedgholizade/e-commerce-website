from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from base.models import BaseModel
from stores.models import Store

User = get_user_model()


class Country(BaseModel):
    """
    Model representing a country.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class City(BaseModel):
    """
    Model representing a city within a country.
    """
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        return f"{self.name}, {self.country.name}"


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
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='addresses',
        null=True,
        blank=True
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def clean(self):
        if not self.user and not self.store:
            raise ValidationError("At least one of user or store must be set.")

    def __str__(self):
        return f"{self.address}, {self.city.name}, {self.city.country.name}"

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation is run before saving
        return super().save(*args, **kwargs)