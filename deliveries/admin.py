"""Admin configuration for the deliveries module."""

from django.contrib import admin

from .models import DeliveryNote


@admin.register(DeliveryNote)
class DeliveryNoteAdmin(admin.ModelAdmin):
    list_display = (
        "delivery_order_number",
        "customer",
        "dispatched_date",
        "driver_name",
        "branch_name",
        "qty_delivered",
        "supervisor_signed",
    )
    list_filter = ("dispatched_date", "supervisor_signed", "branch_name")
    search_fields = ("delivery_order_number", "customer__name", "driver_name")