from django.contrib import admin

from base.admin import BaseAdmin
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(BaseAdmin):
    """
    Admin interface for Payment model.
    """
    list_display = ['order__id',
                    'amount',
                    'status',
                    'transaction_id',
                    'payment_date',
                    'created_at',
                    'updated_at'
                    ]
    search_fields = ['order__id',
                     'transaction_id',
                     'card_pan'
                     ]
    list_filter = BaseAdmin.list_filter + ['status', 'order']
