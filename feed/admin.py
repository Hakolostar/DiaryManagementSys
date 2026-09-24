"""Admin configuration for the feed module."""

from django.contrib import admin

from .models import FeedConsumption, FeedItem, FeedPurchase


@admin.register(FeedItem)
class FeedItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "unit", "cost_per_unit", "reorder_level")
    list_filter = ("category", "unit")
    search_fields = ("name",)


@admin.register(FeedConsumption)
class FeedConsumptionAdmin(admin.ModelAdmin):
    list_display = ("date", "feed_item", "animal", "quantity", "feeding_time")
    list_filter = ("feeding_time", "date")
    search_fields = ("feed_item__name", "animal__tag_number")


@admin.register(FeedPurchase)
class FeedPurchaseAdmin(admin.ModelAdmin):
    list_display = ("purchase_date", "feed_item", "quantity", "unit_cost", "supplier")
    search_fields = ("feed_item__name", "supplier", "invoice_number")