from rest_framework import serializers
from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer used for GET requests.
    Returns full order data including updated_at.
    """
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]


class OrderCreateSerializer(serializers.Serializer):
    """
    Input-only serializer for POST /api/orders/.

    The client only provides an OfferDetail ID.
    All other order fields are derived server-side.
    """
    offer_detail_id = serializers.IntegerField()


class OrderPostResponseSerializer(serializers.ModelSerializer):
    """
    Response serializer used after order creation.

    Differs from OrderSerializer by intentionally
    omitting 'updated_at' to match API specification.
    """
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
        ]