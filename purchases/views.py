"""Views for the purchases module."""

from django.urls import reverse_lazy

from core.views import AppCreateView, AppDeleteView, AppListView, AppUpdateView

from .forms import PurchaseForm, SupplierForm
from .models import Purchase, Supplier


class PurchaseListView(AppListView):
    model = Purchase
    template_name = "purchases/purchase_list.html"
    context_object_name = "purchases"
    title = "Purchases"

    def get_queryset(self):
        return Purchase.objects.select_related("supplier").all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        ctx["total_spend"] = sum(float(p.total) for p in qs)
        ctx["outstanding"] = sum(float(p.balance) for p in qs if p.balance > 0)
        return ctx


class PurchaseAddView(AppCreateView):
    model = Purchase
    form_class = PurchaseForm
    success_url = reverse_lazy("purchases:purchase_list")
    title = "Record Purchase"
    cancel_url = reverse_lazy("purchases:purchase_list")
    success_message = "Purchase recorded."


class PurchaseEditView(AppUpdateView):
    model = Purchase
    form_class = PurchaseForm
    success_url = reverse_lazy("purchases:purchase_list")
    title = "Edit Purchase"
    cancel_url = reverse_lazy("purchases:purchase_list")
    success_message = "Purchase updated."


class PurchaseDeleteView(AppDeleteView):
    model = Purchase
    success_url = reverse_lazy("purchases:purchase_list")
    success_message = "Purchase deleted."


class SupplierListView(AppListView):
    model = Supplier
    template_name = "purchases/supplier_list.html"
    context_object_name = "suppliers"
    title = "Suppliers"


class SupplierAddView(AppCreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = reverse_lazy("purchases:supplier_list")
    title = "Add Supplier"
    cancel_url = reverse_lazy("purchases:supplier_list")
    success_message = "Supplier added."


class SupplierEditView(AppUpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = reverse_lazy("purchases:supplier_list")
    title = "Edit Supplier"
    cancel_url = reverse_lazy("purchases:supplier_list")
    success_message = "Supplier updated."


class SupplierDeleteView(AppDeleteView):
    model = Supplier
    success_url = reverse_lazy("purchases:supplier_list")
    success_message = "Supplier deleted."