"""Views for the inventory module."""

from django.urls import reverse_lazy

from core.views import AppCreateView, AppDeleteView, AppListView, AppUpdateView

from .forms import InventoryItemForm, StockTransactionForm
from .models import InventoryItem, StockTransaction

OUT_TYPES = ("OUT", "ADJUST")


class InventoryListView(AppListView):
    model = InventoryItem
    template_name = "inventory/item_list.html"
    context_object_name = "items"
    title = "Inventory"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["low_stock"] = [
            item for item in InventoryItem.objects.all() if item.is_low
        ]
        ctx["total_value"] = sum(
            float(item.stock_value) for item in InventoryItem.objects.all()
        )
        return ctx


class InventoryAddView(AppCreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    success_url = reverse_lazy("inventory:item_list")
    title = "Add Inventory Item"
    cancel_url = reverse_lazy("inventory:item_list")
    success_message = "Inventory item added."


class InventoryEditView(AppUpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    success_url = reverse_lazy("inventory:item_list")
    title = "Edit Inventory Item"
    cancel_url = reverse_lazy("inventory:item_list")
    success_message = "Inventory item updated."


class InventoryDeleteView(AppDeleteView):
    model = InventoryItem
    success_url = reverse_lazy("inventory:item_list")
    success_message = "Inventory item deleted."


class TransactionListView(AppListView):
    model = StockTransaction
    template_name = "inventory/transaction_list.html"
    context_object_name = "transactions"
    title = "Stock Movements"

    def get_queryset(self):
        return StockTransaction.objects.select_related("item").all()


class TransactionAddView(AppCreateView):
    model = StockTransaction
    form_class = StockTransactionForm
    success_url = reverse_lazy("inventory:transaction_list")
    title = "Record Stock Movement"
    cancel_url = reverse_lazy("inventory:transaction_list")
    success_message = "Stock movement recorded."

    def form_valid(self, form):
        """Keep the item's current_stock in sync with the movement."""
        txn = form.save(commit=False)
        item = txn.item
        if txn.transaction_type == "IN":
            item.current_stock += txn.quantity
        else:
            item.current_stock -= txn.quantity
        if item.current_stock < 0:
            item.current_stock = 0
        item.save()
        return super().form_valid(form)


class TransactionDeleteView(AppDeleteView):
    model = StockTransaction
    success_url = reverse_lazy("inventory:transaction_list")
    success_message = "Stock movement deleted."