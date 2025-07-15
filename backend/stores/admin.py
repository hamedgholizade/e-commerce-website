from django.contrib import admin

from base.admin import BaseAdmin
from stores.models import Store, StoreItem


@admin.register(Store)
class StoreAdmin(BaseAdmin):
    """
    Admin interface for Store model.
    """
    list_display = ['name',
                    'description',
                    'seller__phone',
                    'created_at',
                    'updated_at'
                    ]
    search_fields = ['name', 'description']
    

@admin.register(StoreItem)
class StoreItemAdmin(BaseAdmin):
    """
    Admin interface for StoreItem model.
    """
    list_display = ['store__name',
                    'product__name',
                    'stock',
                    'price',
                    'discount_price',
                    'created_at',
                    'updated_at'
                    ]
    search_fields = ['store__name', 'product__name']
    list_filter = BaseAdmin.list_filter + [
        'store__name',
        'product__name',
        ]
