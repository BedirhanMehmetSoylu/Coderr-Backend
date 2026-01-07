from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a UserProfile instance whenever a new user is created.

    This signal is triggered after a User model instance is saved.
    It ensures that every user in the system always has an associated
    UserProfile object, which prevents null-reference errors throughout
    the application.

    Trigger:
        - post_save signal of the AUTH_USER_MODEL

    Conditions:
        - The profile is only created if the user instance is newly created.

    Args:
        sender (Model):
            The model class that sent the signal (AUTH_USER_MODEL).
        instance (User):
            The actual user instance that was saved.
        created (bool):
            Indicates whether a new record was created.
        **kwargs:
            Additional keyword arguments provided by the signal.

    Side Effects:
        - Creates a UserProfile linked to the newly created user.
        - Initializes all optional profile fields with empty values.
    """
    if created:
        UserProfile.objects.create(
            user=instance,
            first_name="",
            last_name="",
            location="",
            tel="",
            description="",
            working_hours=""
        )
