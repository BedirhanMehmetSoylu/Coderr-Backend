from rest_framework.permissions import BasePermission


class IsReviewOwner(BasePermission):
    """
    Grants object-level access only if the authenticated user
    is the reviewer of the review.
    """
    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
