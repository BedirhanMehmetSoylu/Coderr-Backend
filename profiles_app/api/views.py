from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from ..models import UserProfile
from .serializers import UserProfileSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from .permissions import IsOwner

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a user profile by user ID.

    - GET: Any authenticated user can retrieve a profile
    - PATCH/PUT: Only the owner of the profile may update it
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Resolves the profile by the related user ID instead of profile ID.

        This keeps the API intuitive and stable:
        `/profiles/<user_id>/`

        Raises:
            PermissionDenied:
                - If the profile does not exist
                - If a user attempts to edit a profile they do not own
        """
        user_id = self.kwargs.get("pk")

        try:
            profile = UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            raise NotFound("Profile not found.")

        if self.request.method in ["PATCH"]:
            if profile.user != self.request.user:
                raise PermissionDenied("You may only edit your own profile.")

        return profile

class BusinessProfilesListView(generics.ListAPIView):
    """
    Returns a list of all business profiles.

    Used for browsing available business users.
    """
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns only profiles where the related user
        has the type 'business'.
        """
        return UserProfile.objects.filter(user__type='business')
    
    pagination_class = None

class CustomerProfilesListView(generics.ListAPIView):
    """
    Returns a list of all customer profiles.

    Intended for internal or administrative usage.
    """
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        """
        Returns only profiles where the related user
        has the type 'customer'.
        """
        return UserProfile.objects.filter(user__type='customer')
