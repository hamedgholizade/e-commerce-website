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
                    'slug',
                    'description',
                    'parent',
                    'created_at',
                    'updated_at',
                    ]
    search_fields = ['name', 'slug']
    list_filter = BaseAdmin.list_filter + ['parent']


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    """
    Admin interface for Product model.
    """
    list_display = ['title',
                    'slug',
                    'brand',
                    'status',
                    'created_at',
                    'updated_at',
                    ]
    search_fields = ['title', 'slug', 'brand']
    list_filter = BaseAdmin.list_filter + ['status', 'category__name']
    
    
@admin.register(ProductImage)
class ProductImageAdmin(BaseAdmin):
    """
    Admin interface for ProductImage model.
    """
    list_display = ['product__title',
                    'image',
                    'alt_text',
                    'is_primary',
                    'created_at',
                    'updated_at',
                    ]
    search_fields = ['product__title', 'alt_text']
    list_filter = BaseAdmin.list_filter + ['is_primary']
