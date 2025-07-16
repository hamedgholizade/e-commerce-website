from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from base.admin import BaseAdmin
from accounts.models import User
from accounts.forms import CustomUserCreationForm


@admin.register(User)
class UserAdmin(DjangoUserAdmin, BaseAdmin):
    """
    Admin interface for managing users.
    """
    add_form = CustomUserCreationForm
    model = User
    
    list_display = [
        'phone',
        'email',
        'first_name',
        'last_name',
        'is_seller',
    ]
    search_fields = [
        'phone',
        'email',
        'first_name',
        'last_name'
    ]
    readonly_fields = BaseAdmin.readonly_fields + ['username']
    list_filter = BaseAdmin.list_filter + ['is_seller']
    ordering = ('-created_at',)
    
    #  Fields to be displayed in the user detail view
    fieldsets = (
        (None, {"fields": ("phone", "is_seller", "password")}),
        (_("Personal info"), {"fields": ("email", "picture", "first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    
    #  Fields to be displayed in the add user form for new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone',
                       'email',
                       "picture",
                       'first_name',
                       'last_name',
                       'is_seller',
                       'password1',
                       'password2'),
            }
        ),
    )
    