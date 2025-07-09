from django.contrib import admin

from base.admin import BaseAdmin
from locations.models import Country, City, Address


@admin.register(Country)
class CountryAdmin(BaseAdmin):
    """
    Admin interface for managing countries.
    """
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(City)
class CityAdmin(BaseAdmin):
    """
    Admin interface for managing cities.
    """
    list_display = ['name', 'country', 'created_at', 'updated_at']
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('country',)


@admin.register(Address)
class AddressAdmin(BaseAdmin):
    """
    Admin interface for managing addresses.
    """
    list_display = ['user',
                    'store',
                    'city',
                    'address',
                    'postal_code',
                    'state',
                    'phone',
                    'is_default',
                    'created_at',
                    'updated_at']
    search_fields = ('address', 'postal_code', 'state')
    ordering = ('city__name',)
    list_filter = ['city', 'is_default']
    