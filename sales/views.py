"""Views for the sales module."""

from django.urls import reverse_lazy

from core.views import AppCreateView, AppDeleteView, AppListView, AppUpdateView

from .forms import CustomerForm, SaleForm
from .models import Customer, Sale


class SaleListView(AppListView):
    model = Sale
    template_name = "sales/sale_list.html"
    context_object_name = "sales"
    title = "Sales"

    def get_queryset(self):
        qs = Sale.objects.select_related("customer").all()
        sale_type = self.request.GET.get("type", "")
        if sale_type:
            qs = qs.filter(sale_type=sale_type)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        ctx["type"] = self.request.GET.get("type", "")
        ctx["sale_type_options"] = ["Milk", "Animal", "Product", "Other"]
        ctx["total_revenue"] = sum(float(s.total) for s in qs)
        ctx["outstanding"] = sum(float(s.balance) for s in qs if s.balance > 0)
        return ctx


class SaleAddView(AppCreateView):
    model = Sale
    form_class = SaleForm
    success_url = reverse_lazy("sales:sale_list")
    title = "Record Sale"
    cancel_url = reverse_lazy("sales:sale_list")
    success_message = "Sale recorded."


class SaleEditView(AppUpdateView):
    model = Sale
    form_class = SaleForm
    success_url = reverse_lazy("sales:sale_list")
    title = "Edit Sale"
    cancel_url = reverse_lazy("sales:sale_list")
    success_message = "Sale updated."


class SaleDeleteView(AppDeleteView):
    model = Sale
    success_url = reverse_lazy("sales:sale_list")
    success_message = "Sale deleted."


class CustomerListView(AppListView):
    model = Customer
    template_name = "sales/customer_list.html"
    context_object_name = "customers"
    title = "Customers"


class CustomerAddView(AppCreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy("sales:customer_list")
    title = "Add Customer"
    cancel_url = reverse_lazy("sales:customer_list")
    success_message = "Customer added."


class CustomerEditView(AppUpdateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy("sales:customer_list")
    title = "Edit Customer"
    cancel_url = reverse_lazy("sales:customer_list")
    success_message = "Customer updated."


class CustomerDeleteView(AppDeleteView):
    model = Customer
    success_url = reverse_lazy("sales:customer_list")
    success_message = "Customer deleted."