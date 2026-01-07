from rest_framework import serializers
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review objects.

    - Used for GET, POST, PATCH operations.
    - Read-only fields: id, reviewer, created_at, updated_at
    - Validates rating to ensure it's between 1 and 5
    """
    reviewer = serializers.ReadOnlyField(source="reviewer.id")

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate_rating(self, value):
        """
        Ensures the rating is between 1 and 5 inclusive.
        """
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
