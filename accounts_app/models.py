from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Attributes:
        CUSTOMER (str): Constant representing a customer user type.
        BUSINESS (str): Constant representing a business user type.
        USER_TYPE_CHOICES (list): Available user type choices.
        type (CharField): Stores the type of the user (customer or business).
    """
    CUSTOMER = "customer"
    BUSINESS = "business"

    USER_TYPE_CHOICES = [
        (CUSTOMER, "Customer"),
        (BUSINESS, "Business"),
    ]

    type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
    )

    def __str__(self) -> str:
        """
        String representation of the user.

        Returns:
            str: The username of the user.
        """
        return self.username
