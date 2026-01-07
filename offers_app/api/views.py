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
    """
    Custom pagination class for Offer listings.

    Attributes:
        page_size (int): Default number of offers per page.
        page_size_query_param (str): Query param to override page size.
    """
    page_size = 10
    page_size_query_param = "page_size"


class OfferListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing all offers or creating a new offer.

    GET: List offers with optional filtering and ordering.
    POST: Create a new offer with exactly 3 details (Basic, Standard, Premium).

    Query Params (GET):
        creator_id (int): Filter offers by creator user ID.
        min_price (decimal): Filter offers with details having price >= min_price.
        max_delivery_time (int): Filter offers with details delivery time <= max_delivery_time.
    """
    queryset = Offer.objects.all()
    pagination_class = OfferPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "details__price"]

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on the request method.

        Returns:
            OfferCreateSerializer if POST, otherwise OfferListSerializer.
        """
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def get_permissions(self):
        """
        Return permissions based on the request method.

        POST: Only authenticated business users can create offers.
        GET: Open to any user (no extra permissions).
        """
        if self.request.method == "POST":
            return [IsAuthenticated(), IsBusinessUser()]
        return []

    def get_queryset(self):
        """
        Return the queryset filtered based on query params.

        Filters:
            - creator_id: Offers by a specific user
            - min_price: Offers with details >= min_price
            - max_delivery_time: Offers with details delivery time <= max_delivery_time

        Returns:
            QuerySet: Filtered and distinct offers.
        """
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
    """
    API endpoint to retrieve, update, or delete a specific Offer.

    GET: Retrieve the offer details (any authenticated user).
    PATCH/DELETE: Only the owner of the offer can modify/delete it.
    """
    queryset = Offer.objects.all()

    def get_permissions(self):
        """
        Return permissions based on the request method.

        GET: Only authentication required.
        PATCH/DELETE: Only the offer owner can modify/delete.
        """
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOfferOwner()]

    def get_serializer_class(self):
        """
        Return the serializer class depending on the request method.

        PATCH: Uses OfferUpdateSerializer to allow updating nested details.
        GET/DELETE: Uses OfferListSerializer for read-only output.
        """
        if self.request.method == "PATCH":
            return OfferUpdateSerializer
        return OfferListSerializer
    
    
class OfferDetailDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve a single OfferDetail instance.

    GET: Returns all fields of the OfferDetail.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]


