from django.contrib import admin

from .models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'type',
        'value',
        'start_time',
        'end_time',
        'usage_limit',
        'per_user_limit',
        'is_active',
        'created_at',
        'updated_at',
    )
    search_fields = ['name', 'code']
    list_filter = ['type', 'is_active']
    ordering = ('name',)
    readonly_fields = ['created_at', 'updated_at']
