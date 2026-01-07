from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """
    Allows access only to authenticated users of type 'business'.
    """
    def has_permission(self, request, view):
        """
        Determine if the requesting user is a business user.

        Args:
            request (Request): DRF request object
            view (View): The DRF view

        Returns:
            bool: True if user is authenticated and has type 'business', False otherwise
        """
        return (
            request.user.is_authenticated
            and request.user.type == "business"
        )


class IsOfferOwner(BasePermission):
    """
    Object-level permission to allow only the creator of an Offer to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Determine if the requesting user is the owner of the Offer object.

        Args:
            request (Request): DRF request object
            view (View): The DRF view
            obj (Offer): The Offer instance to check ownership

        Returns:
            bool: True if the user is the creator of the Offer, False otherwise
        """
        return obj.user == request.user
