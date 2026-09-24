"""Sales module models: customers and sales."""

import uuid

from django.db import models

PAYMENT_CHOICES = [("Paid", "Paid"), ("Partial", "Partial"), ("Unpaid", "Unpaid")]


class Customer(models.Model):
    TYPE_CHOICES = [
        ("Individual", "Individual"),
        ("Retailer", "Retailer"),
        ("Cooperative", "Cooperative"),
        ("Other", "Other"),
    ]
    name = models.CharField(max_length=100)
    customer_type = models.CharField(
        max_length=30, choices=TYPE_CHOICES, default="Individual"
    )
    phone = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    address = models.CharField(max_length=200, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Sale(models.Model):
    TYPE_CHOICES = [
        ("Milk", "Milk"),
        ("Animal", "Animal"),
        ("Product", "Product"),
        ("Other", "Other"),
    ]
    sale_number = models.CharField(max_length=30, unique=True, blank=True)
    sale_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="Milk")
    sale_date = models.DateField()
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="sales"
    )
    item_description = models.CharField(max_length=200, blank=True, default="")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, default="Unpaid"
    )
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.quantity * self.unit_price

    @property
    def balance(self):
        return self.total - self.amount_paid

    def save(self, *args, **kwargs):
        if not self.sale_number:
            self.sale_number = f"S-{self.sale_date:%Y%m%d}-{uuid.uuid4().hex[:5].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sale_number} — {self.customer.name} ({self.total})"

    class Meta:
        ordering = ("-sale_date",)