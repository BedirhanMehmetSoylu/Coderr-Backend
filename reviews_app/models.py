from django.conf import settings
from django.db import models


class Review(models.Model):
    """
    Represents a customer review for a business user.

    Each review is linked to:
    - a business user (recipient of the review)
    - a reviewer (customer who wrote the review)

    Constraints:
    - A reviewer can only review a business user once (unique_together)
    - Reviews are ordered by last update timestamp (descending)
    """
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_reviews",
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="written_reviews",
    )
    
    rating = models.PositiveSmallIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Ensures a reviewer cannot review the same business twice.
        Orders reviews by most recent update.
        """
        unique_together = ("business_user", "reviewer")
        ordering = ["-updated_at"]

    def __str__(self):
        """
        Returns a human-readable string representation.
        """
        return f"Review {self.rating} by {self.reviewer_id} for {self.business_user_id}"
