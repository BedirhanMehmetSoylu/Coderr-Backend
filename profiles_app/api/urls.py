from django.urls import path
from .views import UserProfileDetailView, BusinessProfilesListView, CustomerProfilesListView

urlpatterns = [
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/business/', BusinessProfilesListView.as_view(), name='business-profiles'),
    path('profiles/customer/', CustomerProfilesListView.as_view(), name='customer-profiles'),
]
