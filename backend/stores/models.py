from django.db import models
from django.contrib.auth import get_user_model

from base.models import BaseModel
from products.models import Product

User = get_user_model()


class Store(BaseModel):
    """
    Model to represent a store.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(
        User, related_name='stores', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
    

class StoreItem(BaseModel):
    """
    Model to represent an item in a store, linking products to stores.
    """
    store = models.ForeignKey(
        Store, related_name='items', on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name='store_items', on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.title} in {self.store.name}"
