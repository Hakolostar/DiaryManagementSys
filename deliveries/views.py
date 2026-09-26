"""Views for the deliveries module — delivery notes & delivery orders."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DetailView

from core.views import AppCreateView, AppDeleteView, AppListView, AppMixin, AppUpdateView

from .forms import DeliveryNoteForm
from .models import DeliveryNote


class DeliveryNoteListView(AppListView):
    model = DeliveryNote
    template_name = "deliveries/deliverynote_list.html"
    context_object_name = "notes"
    title = "Delivery Notes"

    def get_queryset(self):
        qs = DeliveryNote.objects.select_related("customer").all()
        q = self.request.GET.get("q", "").strip()
        if q:
            from django.db.models import Q

            qs = qs.filter(
                Q(delivery_order_number__icontains=q)
                | Q(customer__name__icontains=q)
                | Q(driver_name__icontains=q)
                | Q(branch_name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["not_invoiced"] = [
            n for n in DeliveryNote.objects.all() if not n.is_invoiced
        ]
        return ctx


class DeliveryNoteDetailView(AppMixin, DetailView):
    model = DeliveryNote
    template_name = "deliveries/deliverynote_detail.html"
    context_object_name = "note"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = f"Delivery Note — {self.object.delivery_order_number}"
        return ctx


class DeliveryNotePrintView(AppMixin, DetailView):
    model = DeliveryNote
    template_name = "deliveries/deliverynote_print.html"
    context_object_name = "note"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = f"Print — {self.object.delivery_order_number}"
        return ctx


class DeliveryNoteCreateView(AppCreateView):
    model = DeliveryNote
    form_class = DeliveryNoteForm
    success_url = reverse_lazy("deliveries:delivery_note_list")
    title = "Create Delivery Note"
    cancel_url = reverse_lazy("deliveries:delivery_note_list")
    success_message = "Delivery note created."


class DeliveryNoteEditView(AppUpdateView):
    model = DeliveryNote
    form_class = DeliveryNoteForm
    success_url = reverse_lazy("deliveries:delivery_note_list")
    title = "Edit Delivery Note"
    cancel_url = reverse_lazy("deliveries:delivery_note_list")
    success_message = "Delivery note updated."


class DeliveryNoteDeleteView(AppDeleteView):
    model = DeliveryNote
    success_url = reverse_lazy("deliveries:delivery_note_list")
    success_message = "Delivery note deleted."


@login_required
def delivery_note_export(request):
    """Export all delivery notes to an .xlsx file."""
    from core.xlsx import build_xlsx_response

    notes = DeliveryNote.objects.select_related("customer")
    headers = [
        "D/O Number", "Customer", "Your Order No", "Order Date", "Dispatched",
        "Driver", "Branch", "Description", "Qty (litres)", "Checked By",
        "Supervisor", "Signed", "Invoiced",
    ]
    rows = [
        [
            n.delivery_order_number, n.customer.name, n.your_order_no,
            n.your_order_date, n.dispatched_date, n.driver_name, n.branch_name,
            n.description_of_goods, float(n.qty_delivered), n.checked_by,
            n.supervisor_name, n.supervisor_signed, "Yes" if n.is_invoiced else "No",
        ]
        for n in notes
    ]
    return build_xlsx_response("delivery-notes", headers, rows)