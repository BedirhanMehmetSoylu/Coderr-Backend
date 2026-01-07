from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """
    Grants access only if the user is a business user
    AND owns the order.
    """
    def has_object_permission(self, request, view, obj):
        """
        Determine if the requesting user is the business owner of the order.

        Args:
            request (Request): DRF request object containing the user
            view (View): The DRF view being accessed
            obj (Order): The Order instance to check ownership

        Returns:
            bool: True if the user is a business user AND is the business_user of the order
        """
        return (
            request.user.type == "business"
            and obj.business_user == request.user
        )
    

class IsCustomerUser(BasePermission):
    """
    Grants access only to authenticated customer users.
    """
    def has_permission(self, request, view):
        """
        Determine if the requesting user is an authenticated customer.

        Args:
            request (Request): DRF request object
            view (View): The DRF view being accessed

        Returns:
            bool: True if the user is authenticated AND has type 'customer'
        """
        return request.user.is_authenticated and request.user.type == "customer"
    

class IsStaffUser(BasePermission):
    """
    Grants access only to staff (admin) users.
    """
    def has_permission(self, request, view):
        """
        Determine if the requesting user is a staff user.

        Args:
            request (Request): DRF request object
            view (View): The DRF view being accessed

        Returns:
            bool: True if the user is a staff member, False otherwise
        """
        return request.user.is_staff


class IsOrderParticipant(BasePermission):
    """
    Grants access if the user is either the customer
    or the business participant of the order.
    """
    def has_object_permission(self, request, view, obj):
        """
        Determine if the requesting user is involved in the order.

        Args:
            request (Request): DRF request object
            view (View): The DRF view being accessed
            obj (Order): The Order instance to check participation

        Returns:
            bool: True if the user is either the customer_user or business_user of the order
        """
        return (
            obj.customer_user == request.user
            or obj.business_user == request.user
        )