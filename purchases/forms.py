"""Forms for the purchases module."""

from core.forms import StyledModelForm

from .models import Purchase, Supplier


class SupplierForm(StyledModelForm):
    class Meta:
        model = Supplier
        fields = ("name", "phone", "email", "address", "notes")


class PurchaseForm(StyledModelForm):
    class Meta:
        model = Purchase
        fields = (
            "purchase_date",
            "supplier",
            "item_name",
            "category",
            "quantity",
            "unit_cost",
            "payment_status",
            "amount_paid",
            "invoice_number",
            "notes",
        )