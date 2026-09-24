"""Admin configuration for the sales module."""

from django.contrib import admin

from .models import Customer, Sale


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "customer_type", "phone", "email")
    list_filter = ("customer_type",)
    search_fields = ("name", "phone", "email")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "sale_number",
        "sale_date",
        "customer",
        "sale_type",
        "quantity",
        "unit_price",
        "payment_status",
    )
    list_filter = ("sale_type", "payment_status", "sale_date")
    search_fields = ("sale_number", "customer__name", "item_description")