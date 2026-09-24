"""Feed module models: feed items, consumption and purchases."""

from django.db import models


class FeedItem(models.Model):
    UNIT_CHOICES = [
        ("kg", "kg"),
        ("L", "L"),
        ("bag", "bag"),
        ("tonne", "tonne"),
        ("Unit", "Unit"),
    ]
    CATEGORY_CHOICES = [
        ("Roughage", "Roughage"),
        ("Concentrate", "Concentrate"),
        ("Mineral", "Mineral"),
        ("Silage", "Silage"),
        ("Other", "Other"),
    ]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=30, choices=CATEGORY_CHOICES, default="Other"
    )
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="kg")
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.name} ({self.unit})"

    class Meta:
        ordering = ("name",)


class FeedConsumption(models.Model):
    FEEDING_TIME_CHOICES = [
        ("Morning", "Morning"),
        ("Afternoon", "Afternoon"),
        ("Evening", "Evening"),
        ("Night", "Night"),
    ]
    animal = models.ForeignKey(
        "herd.Animal",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="feed_records",
        help_text="Leave blank when feeding a herd group",
    )
    date = models.DateField()
    feed_item = models.ForeignKey(
        FeedItem, on_delete=models.CASCADE, related_name="consumptions"
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    feeding_time = models.CharField(
        max_length=20, choices=FEEDING_TIME_CHOICES, default="Morning"
    )
    notes = models.CharField(max_length=200, blank=True, default="")

    @property
    def total_cost(self):
        return self.quantity * (self.cost_per_unit or self.feed_item.cost_per_unit)

    def __str__(self):
        return f"{self.feed_item.name} x {self.quantity} ({self.date})"

    class Meta:
        ordering = ("-date",)


class FeedPurchase(models.Model):
    feed_item = models.ForeignKey(
        FeedItem, on_delete=models.CASCADE, related_name="purchases"
    )
    purchase_date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=100, blank=True, default="")
    invoice_number = models.CharField(max_length=100, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    @property
    def total_cost(self):
        return self.quantity * self.unit_cost

    def __str__(self):
        return f"Purchase {self.feed_item.name} x {self.quantity} ({self.purchase_date})"

    class Meta:
        ordering = ("-purchase_date",)