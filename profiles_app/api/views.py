from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import UserProfile
from .serializers import UserProfileSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from .permissions import IsOwner

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

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
