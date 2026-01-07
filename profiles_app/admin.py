from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile.
    Improves visibility and searchability in Django Admin.
    """
    list_display = ('pk', 'user', 'first_name', 'last_name', 'get_type', 'location', 'tel', 'created_at')
    list_filter = ('user__type',)
    search_fields = ('user__username', 'first_name', 'last_name', 'location', 'tel')

    def get_type(self, obj):
        """
        Returns the user type from the related User model.
        """
        return obj.user.type

    get_type.short_description = 'Type'
