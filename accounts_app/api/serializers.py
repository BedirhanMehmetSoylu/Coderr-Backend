from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Includes password validation, repeated password checking,
    and creation of a user instance.
    """
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "repeated_password",
            "type",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_username(self, value):
        """
        Ensure username does not contain spaces.

        Args:
            value (str): The username to validate.

        Returns:
            str: Validated username.

        Raises:
            serializers.ValidationError: If username contains spaces.
        """
        if " " in value:
            raise serializers.ValidationError("Username cannot contain spaces.")
        return value

    def validate(self, attrs):
        """
        Ensure that password and repeated_password match.

        Args:
            attrs (dict): Input data from request.

        Returns:
            dict: Validated data.

        Raises:
            serializers.ValidationError: If passwords do not match.
        """
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        """
        Create a new user instance with the validated data.

        Args:
            validated_data (dict): Validated input data.

        Returns:
            User: Newly created User instance.
        """
        validated_data.pop("repeated_password")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            type=validated_data["type"],
        )
        return user
