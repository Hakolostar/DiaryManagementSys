"""Forms for the finance module."""

from core.forms import StyledModelForm

from .models import FinanceCategory, Transaction


class CategoryForm(StyledModelForm):
    class Meta:
        model = FinanceCategory
        fields = ("name", "category_type", "description")


class TransactionForm(StyledModelForm):
    class Meta:
        model = Transaction
        fields = (
            "transaction_date",
            "category",
            "description",
            "amount",
            "payment_method",
            "reference_number",
            "notes",
        )