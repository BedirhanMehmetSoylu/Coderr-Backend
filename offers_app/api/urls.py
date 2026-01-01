from django.urls import path
from .views import (
    OfferListCreateView,
    OfferDetailView,
    OfferDetailDetailView,
)

urlpatterns = [
    path("offers/", OfferListCreateView.as_view()),
    path("offers/<int:pk>/", OfferDetailView.as_view()),
    path("offerdetails/<int:pk>/", OfferDetailDetailView.as_view()),
]
