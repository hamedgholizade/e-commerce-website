from django.db import models

from base.models import BaseModel
from orders.models import Order


class Payment(BaseModel):
    """
    Model representing a payment for an order.
    """
    PAYMENT_PENDING = 1
    PAYMENT_SUCCESS = 2
    PAYMENT_FAILED = 3
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'در انتظار پرداخت'),
        (PAYMENT_SUCCESS, 'موفق'),
        (PAYMENT_FAILED, 'ناموفق'),
    ]
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    status = models.PositiveSmallIntegerField(
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_PENDING
    )
    transaction_id = models.CharField(max_length=150)
    amount = models.DecimalField(
        max_digits=15, decimal_places=2
    )
    reference_id = models.CharField(
        max_length=150, blank=True, null=True
    )
    card_pan = models.CharField(
        max_length=20, blank=True, null=True
    )
    fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    payment_date = models.DateTimeField(
        null=True, blank=True
    )

    def __str__(self):
        return f"Payment of {self.amount} for Order {self.order.id}"
