from django.contrib import admin

from base.admin import BaseAdmin
from locations.models import Address


@admin.register(Address)
class AddressAdmin(BaseAdmin):
    """
    Admin interface for managing addresses.
    """
    list_display = ['user',
                    'store',
                    'label',
                    'address_line_1',
                    'city',
                    'state',
                    'postal_code',
                    'created_at',
                    'updated_at']
    search_fields = ('address_line_1', 'postal_code', 'state')
    ordering = ('city',)
    list_filter = BaseAdmin.list_filter + ['city', 'state']
    