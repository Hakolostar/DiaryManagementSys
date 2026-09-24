"""Admin configuration for the accounts app."""

from django.contrib import admin

from .models import FarmProfile


@admin.register(FarmProfile)
class FarmProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "farm_name", "owner_name", "phone", "currency")
    search_fields = ("farm_name", "owner_name", "user__username")