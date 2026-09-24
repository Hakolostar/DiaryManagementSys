"""Forms for the feed module."""

from core.forms import StyledModelForm

from .models import FeedConsumption, FeedItem, FeedPurchase


class FeedItemForm(StyledModelForm):
    class Meta:
        model = FeedItem
        fields = (
            "name",
            "category",
            "unit",
            "cost_per_unit",
            "reorder_level",
            "notes",
        )


class FeedConsumptionForm(StyledModelForm):
    class Meta:
        model = FeedConsumption
        fields = (
            "animal",
            "date",
            "feed_item",
            "quantity",
            "cost_per_unit",
            "feeding_time",
            "notes",
        )


class FeedPurchaseForm(StyledModelForm):
    class Meta:
        model = FeedPurchase
        fields = (
            "feed_item",
            "purchase_date",
            "quantity",
            "unit_cost",
            "supplier",
            "invoice_number",
            "notes",
        )