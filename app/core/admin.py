from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    
    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Fixed tuple format
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
        (_('Important Data'), {'fields': ('last_login',)})  # Fixed syntax
    )

    readonly_fields = ['last_login']  # Moved inside class

    add_fieldsets = (
        (None, {
            'classes': ['wide'],  # Changed set to list
            'fields': (
                'email', 'password1', 'password2', 'name',
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
