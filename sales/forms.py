"""Forms for the sales module."""

from core.forms import StyledModelForm

from .models import Customer, Sale


class CustomerForm(StyledModelForm):
    class Meta:
        model = Customer
        fields = ("name", "customer_type", "phone", "email", "address", "notes")


class SaleForm(StyledModelForm):
    class Meta:
        model = Sale
        fields = (
            "sale_type",
            "sale_date",
            "customer",
            "item_description",
            "quantity",
            "unit_price",
            "payment_status",
            "amount_paid",
            "notes",
        )