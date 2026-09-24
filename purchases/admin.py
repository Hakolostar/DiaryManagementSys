"""Admin configuration for the purchases module."""

from django.contrib import admin

from .models import Purchase, Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email")
    search_fields = ("name", "phone")


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "purchase_number",
        "purchase_date",
        "supplier",
        "item_name",
        "quantity",
        "unit_cost",
        "payment_status",
    )
    list_filter = ("category", "payment_status", "purchase_date")
    search_fields = ("purchase_number", "item_name", "supplier__name")