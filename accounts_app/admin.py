from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    """
    Custom Admin configuration for the User model.
    
    Displays user fields, filters, search, and ordering in the admin panel.
    """
    model = User
    list_display = ('username', 'email', 'type', 'is_staff', 'is_active')
    list_filter = ('type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)
