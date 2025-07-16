from django.contrib import admin

from base.admin import BaseAdmin
from orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    """
    Admin interface for Order model.
    """
    list_display = ['customer__phone',
                    'status', 
                    'total_price',
                    'created_at',
                    'updated_at'
                    ]
    search_fields = ['customer__phone',
                     'customer__first_name',
                     'customer__last_name',
                     'customer__email',
                    'status',
                    ]
    list_filter = BaseAdmin.list_filter + [
        'customer__phone',
        'customer__email',
        'status'
        ]
    

@admin.register(OrderItem)
class OrderItemAdmin(BaseAdmin):
    """
    Admin interface for OrderItem model.
    """
    list_display = ['order__id',
                    'store_item__product',
                    'quantity',
                    'price',
                    'total_price',
                    'created_at',
                    'updated_at'
                    ]
    search_fields = ['order__id',
                     'store_item__product',
                     'order__customer__phone',
                     'store_item__product__name',
                    ]
    list_filter = BaseAdmin.list_filter + [
        'order__status',
        'store_item__product',
        'order__customer__phone',
        'store_item__product__name'
        ]
