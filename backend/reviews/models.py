from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from base.models import BaseModel
from stores.models import Store
from products.models import Product

User = get_user_model()


class Review(BaseModel):
    """
    Model representing a product review.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )
    parent_review = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        blank=True,
        null=True
    )
    comment = models.TextField()
    
    def clean(self):
        if not self.product and not self.store:
            raise ValidationError("At least one of product or store must be set.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation is run before saving
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.user.phone} for {self.product.name}/{self.store.name}"
