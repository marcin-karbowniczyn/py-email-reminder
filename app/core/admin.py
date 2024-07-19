""" Django admin customization """
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models


class UserAdmin(BaseUserAdmin):
    """ Define the admin pages for users """
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Importand dates', {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )
    readonly_fields = ['last_login']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Remainder)
