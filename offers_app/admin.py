from django.contrib import admin
from .models import Offer, OfferDetail

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Offer model.

    Displays key fields in the list view and allows filtering and searching.
    """
    list_display = (
        'id',
        'title',
        'user',
        'created_at',
        'updated_at',
    )
    list_filter = ('created_at', 'updated_at', 'user')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    """
    Admin configuration for the OfferDetail model.

    Displays essential fields, allows filtering by offer type and searching by title.
    """
    list_display = (
        'id',
        'offer',
        'title',
        'offer_type',
        'price',
        'delivery_time_in_days',
        'revisions',
    )
    list_filter = ('offer_type', 'price', 'delivery_time_in_days')
    search_fields = ('title', 'offer__title')
    ordering = ('price',)