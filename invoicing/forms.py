"""Forms for the invoicing module."""

from core.forms import StyledModelForm

from .models import Invoice, InvoiceItem


class InvoiceForm(StyledModelForm):
    class Meta:
        model = Invoice
        fields = (
            "invoice_date",
            "customer",
            "ship_to",
            "delivery_note",
            "driver_name",
            "tax_percent",
            "status",
            "notes",
        )


class InvoiceItemForm(StyledModelForm):
    class Meta:
        model = InvoiceItem
        fields = ("item_code", "description", "quantity", "unit_price")