from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404

from .serializers import ReviewSerializer
from .permissions import IsReviewOwner
from ..models import Review
from profiles_app.models import UserProfile


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    GET:
    Returns a list of reviews.
    Supports filtering by:
    - business_user_id
    - reviewer_id

    POST:
    Creates a new review.
    Only users of type 'customer' can create reviews.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["updated_at", "rating"]
    pagination_class = None

    def get_queryset(self):
        """
        Returns reviews filtered by query parameters if provided.
        """
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get("business_user_id")
        reviewer_id = self.request.query_params.get("reviewer_id")

        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)

        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)

        return queryset

    def perform_create(self, serializer):
        """
        Handles review creation with business logic:

        1. Only customers may create reviews.
        2. Ensures the target business exists and is a business user.
        3. Prevents duplicate reviews by the same reviewer.
        """
        reviewer = self.request.user

        if reviewer.type != "customer":
            raise PermissionDenied("Only customers can create reviews.")

        business_user_id = self.request.data.get("business_user")

        business_profile = get_object_or_404(
            UserProfile,
            user_id=business_user_id,
            user__type="business",
        )

        if Review.objects.filter(
            reviewer=reviewer,
            business_user=business_profile.user,
        ).exists():
            raise PermissionDenied(
                "You have already reviewed this business user."
            )

        serializer.save(
            reviewer=reviewer,
            business_user=business_profile.user,
        )


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles operations on a single review.

    GET:
    Retrieves the review.

    PATCH:
    Updates rating and/or description.
    Only the review owner may edit.

    DELETE:
    Deletes the review.
    Only the review owner may delete.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewOwner]

    def partial_update(self, request, *args, **kwargs):
        """
        Restricts updates to 'rating' and 'description' only.
        Returns 400 if any other field is included.
        """
        allowed_fields = {"rating", "description"}

        invalid_fields = set(request.data.keys()) - allowed_fields
        if invalid_fields:
            raise ValidationError(
                f"Only rating and description can be updated. Invalid fields: {', '.join(invalid_fields)}"
            )

        return super().partial_update(request, *args, **kwargs)