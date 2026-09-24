"""Admin configuration for the inventory module."""

from django.contrib import admin

from .models import InventoryItem, StockTransaction


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "current_stock", "unit", "reorder_level", "unit_cost")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ("item", "transaction_date", "transaction_type", "quantity", "reference")
    list_filter = ("transaction_type", "transaction_date")
    search_fields = ("item__name", "reference")