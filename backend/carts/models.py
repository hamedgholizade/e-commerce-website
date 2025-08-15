from decimal import Decimal, InvalidOperation
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
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.active())
    
    @property
    def total_discount(self):
        total_disc = 0
        for item in self.items.active():
            if hasattr(item.store_item, "discount_price"):
                try:
                    price = Decimal(str(item.store_item.price))
                    disc_price = Decimal(str(item.store_item.discount_price))
                    if disc_price < price:
                        total_disc += (price - disc_price) * item.quantity
                except (InvalidOperation, TypeError):
                    continue
            else:
                continue
        return total_disc

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
        price = self.store_item.discount_price or self.store_item.price
        try:
            return Decimal(str(price))
        except (InvalidOperation, TypeError):
            return Decimal("0")
        
    
    @property
    def total_price(self):
        return self.unit_price * self.quantity
    
    def __str__(self):
        return f"{self.store_item.product.name} in {self.cart.user.phone}'s cart"
