"""Health module models: medicine, vaccination, treatment and vet visits."""

from django.db import models


class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ("Vaccine", "Vaccine"),
        ("Antibiotic", "Antibiotic"),
        ("Dewormer", "Dewormer"),
        ("Vitamin", "Vitamin"),
        ("Antiseptic", "Antiseptic"),
        ("Other", "Other"),
    ]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=30, choices=CATEGORY_CHOICES, default="Other"
    )
    manufacturer = models.CharField(max_length=100, blank=True, default="")
    unit = models.CharField(max_length=30, default="Dose")
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expiry_date = models.DateField(null=True, blank=True)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.name} ({self.category})"

    @property
    def is_low(self):
        return self.reorder_level > 0 and self.stock_quantity > 0 and self.stock_quantity <= self.reorder_level

    class Meta:
        ordering = ("name",)


class Vaccination(models.Model):
    animal = models.ForeignKey(
        "herd.Animal", on_delete=models.CASCADE, related_name="vaccinations"
    )
    vaccine_name = models.CharField(max_length=100)
    date = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    dosage = models.CharField(max_length=50, blank=True, default="")
    administered_by = models.CharField(max_length=100, blank=True, default="")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.animal.full_name} — {self.vaccine_name} ({self.date})"

    class Meta:
        ordering = ("-date",)


class Treatment(models.Model):
    animal = models.ForeignKey(
        "herd.Animal", on_delete=models.CASCADE, related_name="treatments"
    )
    date = models.DateField()
    diagnosis = models.CharField(max_length=200, blank=True, default="")
    treatment_applied = models.TextField(blank=True, default="")
    medicines = models.ManyToManyField(
        Medicine, blank=True, related_name="treatments"
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    veterinarian = models.CharField(max_length=100, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.animal.full_name} — {self.diagnosis or 'Treatment'} ({self.date})"

    class Meta:
        ordering = ("-date",)


class VetVisit(models.Model):
    animal = models.ForeignKey(
        "herd.Animal", on_delete=models.CASCADE, related_name="vet_visits"
    )
    visit_date = models.DateField()
    reason = models.CharField(max_length=200, blank=True, default="")
    findings = models.TextField(blank=True, default="")
    treatment_applied = models.TextField(blank=True, default="")
    vet_name = models.CharField(max_length=100, blank=True, default="")
    follow_up_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.animal.full_name} — {self.reason or 'Visit'} ({self.visit_date})"

    class Meta:
        ordering = ("-visit_date",)