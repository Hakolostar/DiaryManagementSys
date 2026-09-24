"""Views for the feed module — items, consumption, purchases and cost."""

from datetime import date

from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.views import AppCreateView, AppDeleteView, AppListView, AppMixin, AppUpdateView

from .forms import FeedConsumptionForm, FeedItemForm, FeedPurchaseForm
from .models import FeedConsumption, FeedItem, FeedPurchase


class FeedItemListView(AppListView):
    model = FeedItem
    template_name = "feed/item_list.html"
    context_object_name = "items"
    title = "Feed Items"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["total_purchases"] = (
            FeedPurchase.objects.filter(purchase_date__year=date.today().year).aggregate(
                s=Sum("quantity")
            )["s"]
            or 0
        )
        return ctx


class FeedItemAddView(AppCreateView):
    model = FeedItem
    form_class = FeedItemForm
    success_url = reverse_lazy("feed:item_list")
    title = "Add Feed Item"
    cancel_url = reverse_lazy("feed:item_list")
    success_message = "Feed item added."


class FeedItemEditView(AppUpdateView):
    model = FeedItem
    form_class = FeedItemForm
    success_url = reverse_lazy("feed:item_list")
    title = "Edit Feed Item"
    cancel_url = reverse_lazy("feed:item_list")
    success_message = "Feed item updated."


class FeedItemDeleteView(AppDeleteView):
    model = FeedItem
    success_url = reverse_lazy("feed:item_list")
    success_message = "Feed item deleted."


class ConsumptionListView(AppListView):
    model = FeedConsumption
    template_name = "feed/consumption_list.html"
    context_object_name = "records"
    title = "Feed Consumption"


class ConsumptionAddView(AppCreateView):
    model = FeedConsumption
    form_class = FeedConsumptionForm
    success_url = reverse_lazy("feed:consumption_list")
    title = "Record Feed Consumption"
    cancel_url = reverse_lazy("feed:consumption_list")
    success_message = "Consumption recorded."


class ConsumptionEditView(AppUpdateView):
    model = FeedConsumption
    form_class = FeedConsumptionForm
    success_url = reverse_lazy("feed:consumption_list")
    title = "Edit Consumption"
    cancel_url = reverse_lazy("feed:consumption_list")
    success_message = "Consumption updated."


class ConsumptionDeleteView(AppDeleteView):
    model = FeedConsumption
    success_url = reverse_lazy("feed:consumption_list")
    success_message = "Consumption deleted."


class PurchaseListView(AppListView):
    model = FeedPurchase
    template_name = "feed/purchase_list.html"
    context_object_name = "purchases"
    title = "Feed Purchase"


class PurchaseAddView(AppCreateView):
    model = FeedPurchase
    form_class = FeedPurchaseForm
    success_url = reverse_lazy("feed:purchase_list")
    title = "Record Feed Purchase"
    cancel_url = reverse_lazy("feed:purchase_list")
    success_message = "Feed purchase recorded."


class PurchaseEditView(AppUpdateView):
    model = FeedPurchase
    form_class = FeedPurchaseForm
    success_url = reverse_lazy("feed:purchase_list")
    title = "Edit Feed Purchase"
    cancel_url = reverse_lazy("feed:purchase_list")
    success_message = "Feed purchase updated."


class PurchaseDeleteView(AppDeleteView):
    model = FeedPurchase
    success_url = reverse_lazy("feed:purchase_list")
    success_message = "Feed purchase deleted."


class FeedCostView(AppMixin, TemplateView):
    template_name = "feed/cost.html"
    title = "Feed Cost"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        year = int(self.request.GET.get("year", today.year))
        ctx["year"] = year
        ctx["years"] = range(today.year - 3, today.year + 1)
        consumption_records = FeedConsumption.objects.filter(
            date__year=year
        ).select_related("feed_item", "animal")[:400]
        total = sum(float(c.total_cost) for c in consumption_records)
        ctx["consumption_records"] = consumption_records
        ctx["total_consumption_cost"] = total
        purchase_records = FeedPurchase.objects.filter(purchase_date__year=year)[:400]
        ctx["purchase_records"] = purchase_records
        ctx["purchase_cost_total"] = sum(float(p.total_cost) for p in purchase_records)
        ctx["net"] = ctx["purchase_cost_total"] - total
        return ctx