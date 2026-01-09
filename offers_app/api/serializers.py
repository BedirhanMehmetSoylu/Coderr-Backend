from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for OfferDetail model for read-only views.
    """
    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating OfferDetail instances.
    """
    class Meta:
        model = OfferDetail
        fields = [
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferDetailUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating OfferDetail instances.
    """
    class Meta:
        model = OfferDetail
        fields = [
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Offer instances including minimum price, delivery time, 
    and user profile summary.
    """
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_details(self, obj):
        """
        Return list of offer details with URL links.

        Args:
            obj (Offer): Offer instance

        Returns:
            list: List of dictionaries with detail id and URL
        """
        return [
            {"id": detail.id, "url": f"/api/offerdetails/{detail.id}/"}
            for detail in obj.details.all()
        ]

    def get_min_price(self, obj):
        """
        Return the lowest price among all offer details.

        Args:
            obj (Offer)

        Returns:
            Decimal: Minimum price
        """
        return obj.details.order_by("price").first().price

    def get_min_delivery_time(self, obj):
        """
        Return the shortest delivery time among all offer details.

        Args:
            obj (Offer)

        Returns:
            int: Minimum delivery time in days
        """
        return obj.details.order_by("delivery_time_in_days").first().delivery_time_in_days

    def get_user_details(self, obj):
        """
        Return basic info of the user who created the offer.

        Args:
            obj (Offer)

        Returns:
            dict: User info with first_name, last_name, username
        """
        profile = obj.user.profile
        return {
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "username": obj.user.username,
        }
    

class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Offer instances along with nested OfferDetails.

    Validates that exactly 3 OfferDetails exist (Basic, Standard, Premium).
    """
    details = OfferDetailCreateSerializer(many=True)

    class Meta:
        model = Offer
        fields = "__all__"
        read_only_fields = ("user",)

    def validate_details(self, value):
        """
        Ensure exactly 3 details (basic, standard, premium) are provided.

        Args:
            value (list): List of detail dicts

        Raises:
            ValidationError: If not exactly 3 details
        """
        if len(value) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 details."
            )
        return value

    def create(self, validated_data):
        """
        Create an Offer and associated OfferDetail entries.

        Args:
            validated_data (dict): Validated offer data

        Returns:
            Offer: Created offer instance
        """
        details_data = validated_data.pop("details")
        
        user = self.context["request"].user
        offer = Offer.objects.create(user=user, **validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        
        return offer
    

class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Offer and optionally updating nested OfferDetails.
    """
    details = OfferDetailUpdateSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ["title", "description", "image", "details"]

    def update(self, instance, validated_data):
        """
        Update the Offer instance and nested details if provided.

        Args:
            instance (Offer): Offer object to update
            validated_data (dict): Validated data

        Returns:
            Offer: Updated offer
        """
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")

                if not offer_type:
                    raise ValidationError({
                        "details": "Each detail must include 'offer_type'."
                    })

                try:
                    detail = instance.details.get(offer_type=offer_type)
                except OfferDetail.DoesNotExist:
                    raise ValidationError({
                        "details": f"No OfferDetail found for offer_type '{offer_type}'."
                    })

                for attr, value in detail_data.items():
                    setattr(detail, attr, value)
                detail.save()

        return instance

    
class OfferCreateResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for the response of a newly created Offer.

    Returns the Offer along with its nested OfferDetails after creation.
    This matches the API documentation for POST /api/offers/.

    Attributes:
        details (OfferDetailSerializer, many=True): Nested list of OfferDetail objects with full fields.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a single Offer (GET /api/offers/{id}/).

    Returns Offer fields along with nested details URLs, minimum price, and minimum delivery time.
    Matches the API documentation for Offer retrieval.

    Attributes:
        details (SerializerMethodField): Returns a list of OfferDetail objects with 'id' and absolute 'url'.
        min_price (SerializerMethodField): Returns the lowest price among all OfferDetails.
        min_delivery_time (SerializerMethodField): Returns the shortest delivery time among all OfferDetails.
    """
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
        ]

    def get_details(self, obj):
        """
        Build a list of OfferDetail URLs for the retrieved Offer.

        Args:
            obj (Offer): The Offer instance being serialized.

        Returns:
            list: Each item contains the 'id' and absolute 'url' of an OfferDetail.
        """
        request = self.context.get("request")

        return [
            {
                "id": detail.id,
                "url": request.build_absolute_uri(
                    f"/api/offerdetails/{detail.id}/"
                )
                if request
                else f"/api/offerdetails/{detail.id}/",
            }
            for detail in obj.details.all()
        ]

    def get_min_price(self, obj):
        """
        Returns the lowest price among all OfferDetails.

        Args:
            obj (Offer)

        Returns:
            Decimal: Minimum price, or None if no details exist.
        """
        detail = obj.details.order_by("price").first()
        return detail.price if detail else None

    def get_min_delivery_time(self, obj):
        """
        Returns the shortest delivery time among all OfferDetails.

        Args:
            obj (Offer)

        Returns:
            int: Minimum delivery time in days, or None if no details exist.
        """
        detail = obj.details.order_by("delivery_time_in_days").first()
        return detail.delivery_time_in_days if detail else None


class OfferPatchResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for the response after updating an Offer (PATCH /api/offers/{id}/).

    Returns the Offer with all fields, including updated OfferDetails.
    This matches the API documentation for PATCH response.

    Attributes:
        details (OfferDetailSerializer, many=True): Nested OfferDetail objects with full fields, including 'id'.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]
