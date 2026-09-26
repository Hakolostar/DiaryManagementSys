"""Invoicing module models: invoices and their line items."""

import uuid
from datetime import date

from django.db import models

STATUS_CHOICES = [
    ("Draft", "Draft"),
    ("Issued", "Issued"),
    ("Paid", "Paid"),
]


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=30, unique=True, blank=True)
    invoice_date = models.DateField()
    customer = models.ForeignKey(
        "sales.Customer", on_delete=models.CASCADE, related_name="invoices"
    )
    ship_to = models.CharField("Ship to (shop name)", max_length=150, blank=True, default="")
    delivery_note = models.ForeignKey(
        "deliveries.DeliveryNote",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invoices",
        verbose_name="Delivery order reference no.",
    )
    driver_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Auto-filled from the referenced delivery order",
    )
    tax_percent = models.DecimalField(
        "Tax %", max_digits=5, decimal_places=2, default=0,
        help_text="Sales tax / VAT percentage",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Draft")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        return round(sum(float(item.amount) for item in self.items.all()), 2)

    @property
    def tax(self):
        return round(self.subtotal * float(self.tax_percent) / 100, 2)

    @property
    def total(self):
        return round(self.subtotal + self.tax, 2)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = (
                f"INV-{self.invoice_date:%Y%m%d}-{uuid.uuid4().hex[:4].upper()}"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} — {self.customer.name}"

    class Meta:
        ordering = ("-invoice_date", "-created_at")


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="items"
    )
    item_code = models.CharField("Item code", max_length=50, blank=True, default="")
    description = models.CharField("Description", max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(
        "Unit price", max_digits=12, decimal_places=2, default=0
    )

    @property
    def amount(self):
        return float(self.quantity) * float(self.unit_price)

    def __str__(self):
        return f"{self.description} x {self.quantity}"