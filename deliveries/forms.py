"""Forms for the deliveries module."""

from core.forms import StyledModelForm

from .models import DeliveryNote


class DeliveryNoteForm(StyledModelForm):
    class Meta:
        model = DeliveryNote
        fields = (
            "customer",
            "your_order_no",
            "your_order_date",
            "dispatched_date",
            "driver_name",
            "branch_name",
            "description_of_goods",
            "qty_delivered",
            "checked_by",
            "supervisor_name",
            "supervisor_signed",
            "notes",
        )