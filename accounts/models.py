"""Farm profile linked to the Django user account."""

from django.contrib.auth.models import User
from django.db import models


class FarmProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="farm_profile"
    )
    farm_name = models.CharField(max_length=120, blank=True, default="")
    owner_name = models.CharField(max_length=100, blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    address = models.CharField(max_length=200, blank=True, default="")
    currency = models.CharField(max_length=10, default="$", help_text="Currency symbol")
    tagline = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return self.farm_name or self.user.username

    class Meta:
        verbose_name = "Farm profile"
        verbose_name_plural = "Farm profiles"