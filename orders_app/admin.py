from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'customer_user',
        'business_user',
        'status',
        'price',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'offer_type', 'created_at', 'business_user')
    search_fields = ('title', 'customer_user__username', 'business_user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)