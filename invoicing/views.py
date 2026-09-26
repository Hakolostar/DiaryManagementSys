"""Views for the invoicing module — invoices with line items."""

from datetime import date

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView

from core.views import AppCreateView, AppDeleteView, AppListView, AppMixin, AppUpdateView
from deliveries.models import DeliveryNote
from sales.models import Customer

from .forms import InvoiceForm, InvoiceItemForm
from .models import Invoice, InvoiceItem

ItemFormSet = forms.inlineformset_factory(
    Invoice, InvoiceItem, form=InvoiceItemForm, extra=3, can_delete=True
)


class InvoiceListView(AppListView):
    model = Invoice
    template_name = "invoicing/invoice_list.html"
    context_object_name = "invoices"
    title = "Invoices"

    def get_queryset(self):
        qs = Invoice.objects.select_related("customer", "delivery_note").prefetch_related(
            "items"
        )
        status = self.request.GET.get("status", "").strip()
        q = self.request.GET.get("q", "").strip()
        if status:
            qs = qs.filter(status=status)
        if q:
            qs = qs.filter(
                invoice_number__icontains=q, customer__name__icontains=q
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        ctx["status"] = self.request.GET.get("status", "")
        ctx["status_options"] = ["Draft", "Issued", "Paid"]
        ctx["q"] = self.request.GET.get("q", "")
        ctx["total_billed"] = sum(float(i.total) for i in qs)
        return ctx


class InvoiceDetailView(AppMixin, DetailView):
    model = Invoice
    template_name = "invoicing/invoice_detail.html"
    context_object_name = "invoice"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = f"Invoice — {self.object.invoice_number}"
        return ctx


class InvoicePrintView(AppMixin, DetailView):
    model = Invoice
    template_name = "invoicing/invoice_print.html"
    context_object_name = "invoice"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = f"Print — {self.object.invoice_number}"
        return ctx


class InvoiceCreateView(AppCreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "invoicing/invoice_form.html"
    success_url = reverse_lazy("invoicing:invoice_list")
    title = "Create Invoice"
    cancel_url = reverse_lazy("invoicing:invoice_list")
    success_message = "Invoice created."

    def get_initial(self):
        initial = super().get_initial()
        initial["invoice_date"] = date.today()
        do_id = self.request.GET.get("do")
        if do_id:
            do = DeliveryNote.objects.filter(pk=do_id).first()
            if do:
                initial.update(
                    customer=do.customer,
                    ship_to=do.customer.name,
                    delivery_note=do,
                    driver_name=do.driver_name,
                )
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["items_formset"] = ItemFormSet(
            data=self.request.POST if self.request.method == "POST" else None
        )
        ctx["customers"] = Customer.objects.all()
        ctx["delivery_notes"] = DeliveryNote.objects.select_related("customer")
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        items = ctx["items_formset"]
        if items.is_valid():
            self.object = form.save()
            items.instance = self.object
            items.save()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(ctx)


class InvoiceEditView(AppUpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "invoicing/invoice_form.html"
    success_url = reverse_lazy("invoicing:invoice_list")
    title = "Edit Invoice"
    cancel_url = reverse_lazy("invoicing:invoice_list")
    success_message = "Invoice updated."

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["items_formset"] = ItemFormSet(
            instance=self.object,
            data=self.request.POST if self.request.method == "POST" else None,
        )
        ctx["customers"] = Customer.objects.all()
        ctx["delivery_notes"] = DeliveryNote.objects.select_related("customer")
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        items = ctx["items_formset"]
        if items.is_valid():
            items.instance = self.object
            items.save()
            messages.success(self.request, self.success_message)
            return super().form_valid(form)
        return self.render_to_response(ctx)


class InvoiceDeleteView(AppDeleteView):
    model = Invoice
    success_url = reverse_lazy("invoicing:invoice_list")
    success_message = "Invoice deleted."


@login_required
def invoice_export(request):
    """Export invoices (one row per line item) to an .xlsx file."""
    from core.xlsx import build_xlsx_response

    invoices = Invoice.objects.select_related(
        "customer", "delivery_note"
    ).prefetch_related("items")
    headers = [
        "Invoice #", "Invoice Date", "Customer", "Ship To", "D/O Reference",
        "Driver", "Item Code", "Description", "Qty", "Unit Price", "Amount",
        "Subtotal", "Tax", "Total", "Status",
    ]
    rows = []
    for inv in invoices:
        items = list(inv.items.all())
        if not items:
            rows.append([
                inv.invoice_number, inv.invoice_date, inv.customer.name, inv.ship_to,
                getattr(inv.delivery_note, "delivery_order_number", ""), inv.driver_name,
                "", "", "", "", "", inv.subtotal, inv.tax, inv.total, inv.status,
            ])
        for it in items:
            rows.append([
                inv.invoice_number, inv.invoice_date, inv.customer.name, inv.ship_to,
                getattr(inv.delivery_note, "delivery_order_number", ""), inv.driver_name,
                it.item_code, it.description, float(it.quantity), float(it.unit_price),
                round(it.amount, 2), inv.subtotal, inv.tax, inv.total, inv.status,
            ])
    return build_xlsx_response("invoices", headers, rows)