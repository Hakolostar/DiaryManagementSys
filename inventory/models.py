"""Inventory module models: stock items and stock transactions."""

from django.db import models

TRANSACTION_TYPES = [
    ("IN", "Stock In"),
    ("OUT", "Stock Out"),
    ("ADJUST", "Adjustment"),
]


class InventoryItem(models.Model):
    CATEGORY_CHOICES = [
        ("Equipment", "Equipment"),
        ("Feed", "Feed"),
        ("Medicine", "Medicine"),
        ("Supplies", "Supplies"),
        ("Other", "Other"),
    ]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=30, choices=CATEGORY_CHOICES, default="Other"
    )
    unit = models.CharField(max_length=30, default="Unit")
    current_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reorder_level = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    location = models.CharField(max_length=100, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    @property
    def is_low(self):
        return self.reorder_level > 0 and self.current_stock <= self.reorder_level

    @property
    def stock_value(self):
        return self.current_stock * self.unit_cost

    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"

    class Meta:
        ordering = ("name",)


class StockTransaction(models.Model):
    item = models.ForeignKey(
        InventoryItem, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_date = models.DateField()
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_TYPES, default="IN"
    )
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=100, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} {self.item.name} x {self.quantity}"

    class Meta:
        ordering = ("-transaction_date",)