from django.db import models
from django.conf import settings


class Order(models.Model):
    """
    Represents a binding order created by a customer based on an OfferDetail.

    An order connects a customer user with a business user and freezes
    all relevant offer data (price, delivery time, revisions, features)
    at the time of creation.
    """
    STATUS_CHOICES = (
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="customer_orders",
        on_delete=models.CASCADE,
    )

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="business_orders",
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation used in Django admin and debugging.
        """
        return f"Order #{self.id} - {self.title}"