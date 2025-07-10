from django.contrib import admin

from base.admin import BaseAdmin
from orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    """
    Admin interface for Order model.
    """
    list_display = ['user__phone',
                    'discount__name',
                    'status', 
                    'total_price',
                    'created_at',
                    'updated_at'
                    ]
    search_fields = ['user__phone',
                     'user__first_name',
                     'user__last_name',
                     'user__email',
                    'status',
                    ]
    list_filter = BaseAdmin.list_filter + [
        'user__phone',
        'user__email',
        'discount__code',
        'discount__name',
        'status'
        ]
    

@admin.register(OrderItem)
class OrderItemAdmin(BaseAdmin):
    """
    Admin interface for OrderItem model.
    """
    list_display = ['order__id',
                    'store_item__product__name',
                    'quantity',
                    'price_at_purchase',
                    'created_at',
                    'updated_at'
                    ]
    search_fields = ['order__id',
                     'store_item__product__name',
                     'order__user__phone',
                    ]
    list_filter = BaseAdmin.list_filter + [
        'order__status',
        'store_item__product__name',
        'order__user__phone',
        ]
