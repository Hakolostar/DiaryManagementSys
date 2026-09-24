"""Breeding module models: heat, insemination, pregnancy and calving."""

from datetime import timedelta

from django.db import models

HEAT_CYCLE_DAYS = 21


class Heat(models.Model):
    animal = models.ForeignKey(
        "herd.Animal", on_delete=models.CASCADE, related_name="heats"
    )
    heat_date = models.DateField()
    expected_heat_date = models.DateField(null=True, blank=True)
    is_bred = models.BooleanField(default=False)
    detected_by = models.CharField(max_length=100, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.animal.full_name} heat on {self.heat_date}"

    @property
    def due_is_overdue(self):
        if self.expected_heat_date:
            from datetime import date

            return date.today() > self.expected_heat_date
        return False

    class Meta:
        ordering = ("-heat_date",)


class Insemination(models.Model):
    RESULT_CHOICES = [
        ("Pending", "Pending"),
        ("Conceived", "Conceived"),
        ("Not Conceived", "Not Conceived"),
    ]
    animal = models.ForeignKey(
        "herd.Animal", on_delete=models.CASCADE, related_name="inseminations"
    )
    service_date = models.DateField()
    bull_name = models.CharField(max_length=100, blank=True, default="")
    bull_breed = models.CharField(max_length=100, blank=True, default="")
    semen_source = models.CharField(max_length=100, blank=True, default="")
    technician = models.CharField(max_length=100, blank=True, default="")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    result = models.CharField(
        max_length=30, choices=RESULT_CHOICES, default="Pending"
    )
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"AI {self.animal.full_name} on {self.service_date}"

    class Meta:
        ordering = ("-service_date",)


class Pregnancy(models.Model):
    DIAGNOSIS_CHOICES = [
        ("Positive", "Positive"),
        ("Negative", "Negative"),
        ("Unconfirmed", "Unconfirmed"),
    ]
    animal = models.ForeignKey(
        "herd.Animal", on_delete=models.CASCADE, related_name="pregnancy_checks"
    )
    insemination = models.ForeignKey(
        Insemination,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pregnancy_checks",
    )
    check_date = models.DateField()
    diagnosis = models.CharField(
        max_length=30, choices=DIAGNOSIS_CHOICES, default="Unconfirmed"
    )
    expected_calving_date = models.DateField(null=True, blank=True)
    confirmed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")

    @property
    def is_overdue(self):
        if not self.expected_calving_date:
            return False
        from datetime import date

        return date.today() > self.expected_calving_date

    def __str__(self):
        return f"{self.animal.full_name} — {self.diagnosis} ({self.check_date})"

    class Meta:
        ordering = ("-check_date",)


class Calving(models.Model):
    TYPE_CHOICES = [
        ("Single", "Single"),
        ("Twin", "Twin"),
        ("Triplets", "Triplets"),
    ]
    COMPLICATION_CHOICES = [
        ("None", "None"),
        ("Mild", "Mild"),
        ("Severe", "Severe"),
        ("Dead Calf", "Dead Calf"),
    ]
    animal = models.ForeignKey(
        "herd.Animal", on_delete=models.CASCADE, related_name="calvings"
    )
    calving_date = models.DateField()
    calving_type = models.CharField(
        max_length=30, choices=TYPE_CHOICES, default="Single"
    )
    male_calves = models.PositiveSmallIntegerField(default=0)
    female_calves = models.PositiveSmallIntegerField(default=0)
    complication = models.CharField(
        max_length=30, choices=COMPLICATION_CHOICES, default="None"
    )
    vet_name = models.CharField(max_length=100, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.animal.full_name} calved {self.calving_type} ({self.calving_date})"

    class Meta:
        ordering = ("-calving_date",)