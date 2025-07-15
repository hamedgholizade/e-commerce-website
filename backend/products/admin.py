from django.contrib import admin

from base.admin import BaseAdmin
from products.models import (
    Category,
    Product,
    ProductImage,
    )


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    """
    Admin interface for Category model.
    """
    list_display = ['name',
                    'description',
                    'parent',
                    'created_at',
                    'updated_at',
                    ]
    search_fields = ['name', 'description']
    list_filter = BaseAdmin.list_filter + ['parent']


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    """
    Admin interface for Product model.
    """
    list_display = ['name',
                    'stock',
                    'rating',
                    'created_at',
                    'updated_at',
                    ]
    search_fields = ['name', 'description']
    list_filter = BaseAdmin.list_filter + ['category__name']
    
    
@admin.register(ProductImage)
class ProductImageAdmin(BaseAdmin):
    """
    Admin interface for ProductImage model.
    """
    list_display = ['product__name',
                    'image',
                    'created_at',
                    'updated_at',
                    ]
    search_fields = ('product__name',)
    list_filter = BaseAdmin.list_filter + ['product__name']
