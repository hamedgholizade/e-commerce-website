from django.contrib import admin

from base.admin import BaseAdmin
from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(BaseAdmin):
    """
    Admin interface for Review model.
    """
    list_display = ['user__phone',
                    'product__name',
                    'store__name',
                    'created_at',
                    'updated_at'
                    ]
    search_fields = ['user__phone',
                     'product__name',
                     'store__name'
                     ]
    list_filter = BaseAdmin.list_filter + ['user__phone', 'product', 'store']
