"""Finance module models: categories and transactions."""

from django.db import models


class FinanceCategory(models.Model):
    TYPE_CHOICES = [("Income", "Income"), ("Expense", "Expense")]
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return f"{self.name} ({self.category_type})"

    class Meta:
        ordering = ("category_type", "name")
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category_type"], name="unique_finance_category"
            )
        ]


class Transaction(models.Model):
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("Bank Transfer", "Bank Transfer"),
        ("Mobile Money", "Mobile Money"),
        ("Card", "Card"),
        ("Cheque", "Cheque"),
    ]
    transaction_date = models.DateField()
    category = models.ForeignKey(
        FinanceCategory, on_delete=models.PROTECT, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.CharField(max_length=200, blank=True, default="")
    payment_method = models.CharField(
        max_length=30, choices=PAYMENT_CHOICES, default="Cash"
    )
    reference_number = models.CharField(max_length=100, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_income(self):
        return self.category.category_type == "Income"

    def __str__(self):
        return f"{self.category.category_type}: {self.amount} ({self.transaction_date})"

    class Meta:
        ordering = ("-transaction_date", "-created_at")