"""Milk production module models: production, lactation, quality, targets."""

from django.core.validators import MinValueValidator
from django.db import models

SESSION_CHOICES = [("Morning", "Morning"), ("Evening", "Evening")]


class Lactation(models.Model):
    animal = models.ForeignKey(
        "herd.Animal", on_delete=models.CASCADE, related_name="lactations"
    )
    lactation_number = models.PositiveIntegerField(default=1)
    start_date = models.DateField()
    dry_off_date = models.DateField(null=True, blank=True)
    expected_dry_off = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")

    @property
    def is_active(self):
        return self.dry_off_date is None

    def __str__(self):
        return f"{self.animal.full_name} — Lactation {self.lactation_number}"

    class Meta:
        ordering = ("animal", "-lactation_number")
        constraints = [
            models.UniqueConstraint(
                fields=["animal", "lactation_number"],
                name="unique_lactation_per_animal",
            )
        ]


class MilkProduction(models.Model):
    animal = models.ForeignKey(
        "herd.Animal", on_delete=models.CASCADE, related_name="milk_records"
    )
    date = models.DateField()
    session = models.CharField(max_length=10, choices=SESSION_CHOICES)
    quantity = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    notes = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.animal.full_name} {self.session} {self.quantity} L ({self.date})"

    class Meta:
        ordering = ("-date", "-session")
        constraints = [
            models.UniqueConstraint(
                fields=["animal", "date", "session"],
                name="unique_production_per_session",
            )
        ]


class MilkQuality(models.Model):
    animal = models.ForeignKey(
        "herd.Animal", on_delete=models.CASCADE, related_name="milk_quality_records"
    )
    date = models.DateField()
    fat_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    protein_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    snf_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    density = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    temperature = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    remarks = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return f"{self.animal.full_name} — {self.date} (Fat {self.fat_pct}%)"

    class Meta:
        ordering = ("-date",)
        constraints = [
            models.UniqueConstraint(
                fields=["animal", "date"], name="unique_quality_per_day"
            )
        ]


class YieldTarget(models.Model):
    animal = models.OneToOneField(
        "herd.Animal", on_delete=models.CASCADE, related_name="yield_target"
    )
    target_daily_liters = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.animal.full_name}: {self.target_daily_liters} L/day"

    class Meta:
        verbose_name = "Yield target"
        verbose_name_plural = "Yield targets"