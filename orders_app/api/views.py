from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q
from django.shortcuts import get_object_or_404

from ..models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, OrderPostResponseSerializer
from offers_app.models import OfferDetail
from profiles_app.models import UserProfile
from .permissions import (
    IsBusinessUser,
    IsStaffUser,
    IsOrderParticipant,
    IsCustomerUser
)


class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET:
    Returns all orders where the authenticated user is either
    the customer or the business partner.

    POST:
    Creates a new order based on an OfferDetail.
    Only users of type 'customer' are allowed.
    """
    pagination_class = None

    def get_permissions(self):
        """
        Dynamically assigns permissions based on HTTP method.
        """
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Limits visible orders to those related to the authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )

    def get_serializer_class(self):
        """
        Uses a lightweight serializer for POST
        and a full serializer for GET.
        """
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles order creation.

        Business logic:
        - Validate offer_detail_id
        - Copy all relevant fields from OfferDetail
        - Persist a new Order instance
        """
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer_detail = get_object_or_404(
            OfferDetail,
            id=serializer.validated_data["offer_detail_id"]
        )

        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )

        return Response(
            OrderPostResponseSerializer(order).data,
            status=201
        )


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles single-order operations.

    GET:
    Accessible to both customer and business participant.

    PATCH:
    Only business users may update the order status.

    DELETE:
    Restricted to staff users only.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        """
        Assigns permissions based on HTTP method.
        """
        if self.request.method == "PATCH":
            return [IsAuthenticated(), IsBusinessUser()]
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsStaffUser()]
        return [IsAuthenticated(), IsOrderParticipant()]

    def partial_update(self, request, *args, **kwargs):
        """
        Allows updating only the 'status' field.

        Any other payload structure results in a 400 Bad Request.
        """
        if set(request.data.keys()) != {"status"}:
            raise ValidationError({"status": "Only status can be updated."})

        if request.data["status"] not in ["in_progress", "completed", "cancelled"]:
            raise ValidationError({"status": "Invalid status value."})

        return super().partial_update(request, *args, **kwargs)

class OrderCountView(APIView):
    """
    Returns the number of active (in_progress) orders
    for a specific business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """
        Validates business user existence and returns count.
        """
        get_object_or_404(
            UserProfile,
            user_id=business_user_id,
            user__type="business",
        )

        count = Order.objects.filter(
            business_user_id=business_user_id,
            status="in_progress",
        ).count()

        return Response({"order_count": count})


class CompletedOrderCountView(APIView):
    """
    Returns the number of completed orders
    for a specific business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """
        Validates business user existence and returns count.
        """
        get_object_or_404(
            UserProfile,
            user_id=business_user_id,
            user__type="business",
        )

        count = Order.objects.filter(
            business_user_id=business_user_id,
            status="completed",
        ).count()

        return Response({"completed_order_count": count})