from django.db import models
from django.contrib.auth import get_user_model

from base.models import BaseModel
from locations.models import Address
from discounts.models import Discount
from stores.models import StoreItem

User = get_user_model()


class Order(BaseModel):
    """
    Model representing an order in the e-commerce system.
    """
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders'
        )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name='orders'
        )
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
        )
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default='pending'
        )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, blank=True, null=True
        )
    
    def __str__(self):
        return f"""
                Order {self.id} by {self.user.phone}/
                {self.user.first_name}.{self.user.last_name}
                - Status: {self.status}"""


class OrderItem(BaseModel):
    """
    Model representing an item in an order.
    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
        )
    store_item = models.ForeignKey(
        StoreItem, on_delete=models.CASCADE, related_name='order_items'
        )
    quantity = models.PositiveIntegerField(default=0)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"""
                Item {self.id} in Order 
                {self.order.id} - {self.store_item.product.title}
                x {self.quantity}"""
