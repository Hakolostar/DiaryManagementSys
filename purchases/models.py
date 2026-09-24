"""Purchases module models: suppliers and purchases."""

import uuid

from django.db import models

from sales.models import PAYMENT_CHOICES


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    address = models.CharField(max_length=200, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Purchase(models.Model):
    CATEGORY_CHOICES = [
        ("Equipment", "Equipment"),
        ("Feed", "Feed"),
        ("Medicine", "Medicine"),
        ("Office", "Office"),
        ("Other", "Other"),
    ]
    purchase_number = models.CharField(max_length=30, unique=True, blank=True)
    purchase_date = models.DateField()
    supplier = models.ForeignKey(
        Supplier, null=True, blank=True, on_delete=models.SET_NULL, related_name="purchases"
    )
    item_name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=30, choices=CATEGORY_CHOICES, default="Other"
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, default="Unpaid"
    )
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    invoice_number = models.CharField(max_length=100, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.quantity * self.unit_cost

    @property
    def balance(self):
        return self.total - self.amount_paid

    def save(self, *args, **kwargs):
        if not self.purchase_number:
            self.purchase_number = (
                f"P-{self.purchase_date:%Y%m%d}-{uuid.uuid4().hex[:5].upper()}"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.purchase_number} — {self.item_name} ({self.total})"

    class Meta:
        ordering = ("-purchase_date",)