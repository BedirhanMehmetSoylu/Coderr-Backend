from rest_framework import serializers
from ..models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
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
        if obj.file:
            return obj.file.url
        return ""
    
    
class BusinessProfileSerializer(serializers.ModelSerializer):
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
        if obj.file:
            return obj.file.url
        return ""


class CustomerProfileSerializer(serializers.ModelSerializer):
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
        if obj.file:
            return obj.file.url
        return ""