"""Delivery Note / Delivery Order module models."""

import uuid
from datetime import date

from django.db import models


class DeliveryNote(models.Model):
    """A delivery order note dispatched to a customer."""

    delivery_order_number = models.CharField(
        "Delivery order number", max_length=30, unique=True, blank=True
    )
    customer = models.ForeignKey(
        "sales.Customer",
        on_delete=models.CASCADE,
        related_name="delivery_notes",
        verbose_name="Customer / To",
    )
    your_order_no = models.CharField("Your order no.", max_length=100, blank=True, default="")
    your_order_date = models.DateField("Your order date", null=True, blank=True)
    dispatched_date = models.DateField("Date dispatched", null=True, blank=True)
    driver_name = models.CharField("Driver name", max_length=100, blank=True, default="")
    branch_name = models.CharField("Branch name", max_length=100, blank=True, default="")
    description_of_goods = models.TextField(
        "Description of goods", blank=True, default="Fresh milk delivery"
    )
    qty_delivered = models.DecimalField(
        "Qty delivered (litres)", max_digits=12, decimal_places=2, default=0
    )
    checked_by = models.CharField("Checked by", max_length=100, blank=True, default="")
    supervisor_name = models.CharField(
        "Supervisor name", max_length=100, blank=True, default=""
    )
    supervisor_signed = models.BooleanField(
        "Supervisor signature", default=False,
        help_text="Tick when the supervisor has signed",
    )
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_invoiced(self):
        return self.invoices.exists()

    @property
    def signature_status(self):
        return "Signed" if self.supervisor_signed else "Pending"

    def save(self, *args, **kwargs):
        if not self.delivery_order_number:
            self.delivery_order_number = (
                f"D/O-{date.today():%Y%m%d}-{uuid.uuid4().hex[:4].upper()}"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.delivery_order_number} — {self.customer.name}"

    class Meta:
        ordering = ("-dispatched_date", "-created_at")
        verbose_name = "Delivery Note"
        verbose_name_plural = "Delivery Notes"