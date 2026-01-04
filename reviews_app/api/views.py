from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404

from .serializers import ReviewSerializer
from .permissions import IsReviewOwner
from ..models import Review
from profiles_app.models import UserProfile


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["updated_at", "rating"]
    pagination_class = None

    def get_queryset(self):
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get("business_user_id")
        reviewer_id = self.request.query_params.get("reviewer_id")

        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)

        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)

        return queryset

    def perform_create(self, serializer):
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
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewOwner]

    def partial_update(self, request, *args, **kwargs):
        allowed_fields = {"rating", "description"}

        invalid_fields = set(request.data.keys()) - allowed_fields
        if invalid_fields:
            raise ValidationError(
                f"Only rating and description can be updated. Invalid fields: {', '.join(invalid_fields)}"
            )

        return super().partial_update(request, *args, **kwargs)