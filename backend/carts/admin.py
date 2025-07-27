from django.contrib import admin

from base.admin import BaseAdmin
from carts.models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(BaseAdmin):
    """
    Admin interface for Cart model.
    """
    list_display = ['user__phone',
                    'total_price',
                    'created_at',
                    'updated_at'
                    ]
    search_fields = ['user__phone',
                     'user__email'
                    ]
    list_filter = BaseAdmin.list_filter + ['user']


@admin.register(CartItem)
class CartItemAdmin(BaseAdmin):
    """
    Admin interface for CartItem model.
    """
    list_display = ['cart__user__phone',
                    'store_item__product__name',
                    'quantity',
                    'unit_price',
                    'total_price',
                    'created_at',
                    'updated_at'
                    ]
    search_fields = ['cart__user__phone',
                     'store_item__product__name'
                     ]
    list_filter = BaseAdmin.list_filter + ['cart', 'store_item']
