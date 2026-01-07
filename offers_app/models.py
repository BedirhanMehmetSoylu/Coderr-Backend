from django.conf import settings
from django.db import models


class Offer(models.Model):
    """
    Represents a business offer created by a user.

    Attributes:
        user (ForeignKey): The user who created the offer.
        title (str): The title of the offer.
        image (ImageField): Optional image representing the offer.
        description (str): Description of the offer.
        created_at (datetime): Timestamp when the offer was created.
        updated_at (datetime): Timestamp when the offer was last updated.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="offers"
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offers/", null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        """
        API endpoint to retrieve a single OfferDetail instance.

        GET: Returns all fields of the OfferDetail.
        """
        return self.title


class OfferDetail(models.Model):
    """
    Represents the specific tiers/details of an Offer (Basic, Standard, Premium).

    Attributes:
        offer (ForeignKey): The parent Offer this detail belongs to.
        title (str): Title of the offer detail.
        revisions (int): Number of revisions included.
        delivery_time_in_days (int): Delivery time in days.
        price (Decimal): Price of the offer detail.
        features (list): JSON list of features included.
        offer_type (str): Tier type ('basic', 'standard', 'premium').
    """
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"

    OFFER_TYPE_CHOICES = [
        (BASIC, "Basic"),
        (STANDARD, "Standard"),
        (PREMIUM, "Premium"),
    ]

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="details"
    )
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        """
        Return a string showing the offer title and its type.
        """
        return f"{self.offer.title} – {self.offer_type}"
