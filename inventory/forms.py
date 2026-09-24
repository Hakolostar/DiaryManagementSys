"""Forms for the inventory module."""

from core.forms import StyledModelForm

from .models import InventoryItem, StockTransaction


class InventoryItemForm(StyledModelForm):
    class Meta:
        model = InventoryItem
        fields = (
            "name",
            "category",
            "unit",
            "current_stock",
            "reorder_level",
            "unit_cost",
            "location",
            "notes",
        )


class StockTransactionForm(StyledModelForm):
    class Meta:
        model = StockTransaction
        fields = (
            "item",
            "transaction_date",
            "transaction_type",
            "quantity",
            "reference",
            "notes",
        )