from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Review model.
    """
    list_display = (
        'id',
        'reviewer',
        'business_user',
        'rating',
        'created_at',
        'updated_at',
    )
    list_filter = ('rating', 'created_at', 'business_user')
    search_fields = ('reviewer__username', 'business_user__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)