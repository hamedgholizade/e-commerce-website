from django.db import models
from django.contrib.auth import get_user_model

from base.models import BaseModel
from stores.models import StoreItem

User = get_user_model()


class Cart(BaseModel):
    """
    Model representing a shopping cart.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    total_price = models.CharField(
        max_length=100, blank=True, null=True
    )
    
    @property
    def total_price(self):
        self.total_price = sum(self.items.total_price())
        return self.total_price

    def __str__(self):
        return f"Cart of {self.user.phone}"


class CartItem(BaseModel):
    """
    Model representing an item in a shopping cart.
    """
    
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    store_item = models.ForeignKey(
        StoreItem,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)

    @property
    def unit_price(self):
        if self.store_item.discount_price:
            return self.store_item.discount_price
        return self.store_item.price
    
    @property
    def total_price(self):
        return float(self.unit_price) * self.quantity
    
    def __str__(self):
        return f"{self.store_item.product.name} in {self.cart.user.phone}'s cart"
