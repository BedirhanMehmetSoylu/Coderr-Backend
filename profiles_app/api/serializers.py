from rest_framework import serializers
from ..models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Full profile serializer used for:
    - retrieving a user's own profile
    - updating a user's own profile

    Includes user-related fields via serializer source mapping.
    """
    first_name = serializers.CharField(default="", allow_blank=True)
    last_name = serializers.CharField(default="", allow_blank=True)
    location = serializers.CharField(default="", allow_blank=True)
    tel = serializers.CharField(default="", allow_blank=True)
    description = serializers.CharField(default="", allow_blank=True)
    working_hours = serializers.CharField(default="", allow_blank=True)
    file = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    type = serializers.CharField(source='user.type')

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'email',
            'created_at'
        ]

    def get_file(self, obj):
        """
        Returns the absolute URL of the profile image if present.
        Returns an empty string otherwise to avoid null values in the frontend.
        """
        if obj.file:
            return obj.file.url
        return ""
    
    
class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for public business profiles.

    Used when listing business users.
    Does NOT expose email for privacy reasons.
    """
    first_name = serializers.CharField(default="", allow_blank=True)
    last_name = serializers.CharField(default="", allow_blank=True)
    location = serializers.CharField(default="", allow_blank=True)
    tel = serializers.CharField(default="", allow_blank=True)
    description = serializers.CharField(default="", allow_blank=True)
    working_hours = serializers.CharField(default="", allow_blank=True)
    file = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username')
    type = serializers.CharField(source='user.type')

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
        ]

    def get_file(self, obj):
        """
        Returns the profile image URL if available.
        """
        if obj.file:
            return obj.file.url
        return ""


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for customer profiles.

    Used for listing customers.
    Only exposes minimal personal data.
    """
    first_name = serializers.CharField(default="", allow_blank=True)
    last_name = serializers.CharField(default="", allow_blank=True)
    file = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username')
    type = serializers.CharField(source='user.type')

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'type',
        ]

    def get_file(self, obj):
        """
        Returns the absolute URL of the profile image if present.
        Returns an empty string otherwise to avoid null values in the frontend.
        """
        if obj.file:
            return obj.file.url
        return ""