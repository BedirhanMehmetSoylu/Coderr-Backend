from rest_framework import serializers
from ..models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
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
        return [
            {"id": detail.id, "url": f"/api/offerdetails/{detail.id}/"}
            for detail in obj.details.all()
        ]

    def get_min_price(self, obj):
        return obj.details.order_by("price").first().price

    def get_min_delivery_time(self, obj):
        return obj.details.order_by("delivery_time_in_days").first().delivery_time_in_days

    def get_user_details(self, obj):
        profile = obj.user.profile
        return {
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "username": obj.user.username,
        }
    

class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailCreateSerializer(many=True)

    class Meta:
        model = Offer
        fields = "__all__"
        read_only_fields = ("user",)

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 details."
            )
        return value

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        
        user = self.context["request"].user
        offer = Offer.objects.create(user=user, **validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        
        return offer
    

class OfferUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailUpdateSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ["title", "description", "image", "details"]

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")

                detail = instance.details.get(offer_type=offer_type)

                for attr, value in detail_data.items():
                    setattr(detail, attr, value)
                detail.save()

        return instance