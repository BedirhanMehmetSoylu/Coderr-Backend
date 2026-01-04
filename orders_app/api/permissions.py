from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.type == "business"
            and obj.business_user == request.user
        )
    

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == "customer"
    

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsOrderParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.customer_user == request.user
            or obj.business_user == request.user
        )