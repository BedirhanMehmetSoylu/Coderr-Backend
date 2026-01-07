from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to allow access only to the owner.

    Used when a resource belongs directly to a user.
    """
    def has_object_permission(self, request, view, obj):
        """
        Checks whether the authenticated user owns the profile.
        """
        return obj.user == request.user