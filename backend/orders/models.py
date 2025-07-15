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
    ORDER_PENDING = 1
    ORDER_PROCCESSING = 2
    ORDER_DELIVERED = 3
    ORDER_CANCELLED = 4
    ORDER_FAILED = 5
    
    ORDER_STATUS_CHOICES = [
        (ORDER_PENDING, 'منتظر'),
        (ORDER_PROCCESSING, 'در حال پردازش'),
        (ORDER_DELIVERED, 'تحویل شده'),
        (ORDER_CANCELLED, 'لغو شده'),
        (ORDER_FAILED, 'خطا'),
    ]
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders'
        )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name='orders'
        )
    status = models.IntegerField(
        choices=ORDER_STATUS_CHOICES, default=ORDER_PENDING
        )
    total_price = models.CharField(
        max_length=100, blank=True, null=True
        )
    
    def __str__(self):
        return f"""
                Order {self.id} by {self.customer.phone}/
                {self.customer.first_name}.{self.customer.last_name}
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
    price = models.CharField(
        max_length=100, blank=True, null=True
        )
    total_price = models.CharField(
        max_length=100, blank=True, null=True
        )

    def __str__(self):
        return f"""
                Item {self.id} in Order 
                {self.order.id} - {self.store_item.product.name}
                x {self.quantity}"""
