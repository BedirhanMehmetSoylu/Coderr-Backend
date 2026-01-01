from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    OfferListSerializer,
    OfferCreateSerializer,
    OfferUpdateSerializer,
    OfferDetailSerializer,
)
from .permissions import IsBusinessUser, IsOfferOwner
from ..models import Offer, OfferDetail


class OfferPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    pagination_class = OfferPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "details__price"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsBusinessUser()]
        return []

    def get_queryset(self):
        queryset = super().get_queryset()

        creator_id = self.request.query_params.get("creator_id")
        min_price = self.request.query_params.get("min_price")
        max_delivery_time = self.request.query_params.get("max_delivery_time")

        if creator_id:
            queryset = queryset.filter(user_id=creator_id)

        if min_price:
            queryset = queryset.filter(details__price__gte=min_price)

        if max_delivery_time:
            queryset = queryset.filter(
                details__delivery_time_in_days__lte=max_delivery_time
            )

        return queryset.distinct()
    
    
class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOfferOwner()]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return OfferUpdateSerializer
        return OfferListSerializer
    
    
class OfferDetailDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]


