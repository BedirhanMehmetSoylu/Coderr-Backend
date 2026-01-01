from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..models import UserProfile
from .serializers import UserProfileSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from .permissions import IsOwner

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get("pk")

        try:
            profile = UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("Profile not found.")

        if self.request.method in ["PATCH", "PUT"]:
            if profile.user != self.request.user:
                raise PermissionDenied("You may only edit your own profile.")

        return profile

class BusinessProfilesListView(generics.ListAPIView):
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user__type='business')
    
    pagination_class = None

class CustomerProfilesListView(generics.ListAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return UserProfile.objects.filter(user__type='customer')
