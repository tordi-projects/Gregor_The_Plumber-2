from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extra customer details attached to Django's built-in User model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    phone_number = models.CharField(max_length=20, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
