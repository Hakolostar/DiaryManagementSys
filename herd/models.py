"""Herd module models: animals, breeds and animal movements."""

from django.db import models
from django.urls import reverse

SEX_CHOICES = [("Female", "Female"), ("Male", "Male")]
CATEGORY_CHOICES = [
    ("Calf", "Calf"),
    ("Heifer", "Heifer"),
    ("Milker", "Milker"),
    ("Dry", "Dry"),
    ("Weaner", "Weaner"),
    ("Yearling", "Yearling"),
    ("Bulling", "Bulling"),
    ("Bull", "Bull"),
    ("Steer", "Steer"),
]
STATUS_CHOICES = [
    ("Active", "Active"),
    ("Sold", "Sold"),
    ("Culled", "Culled"),
    ("Deceased", "Deceased"),
    ("Transferred", "Transferred"),
]
SOURCE_CHOICES = [
    ("Born", "Born"),
    ("Purchased", "Purchased"),
    ("Transferred In", "Transferred In"),
]
MOVEMENT_CHOICES = [
    ("Barn Transfer", "Barn Transfer"),
    ("Pasture", "Pasture"),
    ("Purchased", "Purchased"),
    ("Sold", "Sold"),
    ("Transferred Out", "Transferred Out"),
    ("Deceased", "Deceased"),
]


class Breed(models.Model):
    name = models.CharField(max_length=100, unique=True)
    purpose = models.CharField(max_length=100, blank=True, default="")
    origin = models.CharField(max_length=100, blank=True, default="")
    avg_milk_yield = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, help_text="Average litres per day"
    )
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Animal(models.Model):
    tag_number = models.CharField("Tag number", max_length=30, unique=True)
    name = models.CharField(max_length=100, blank=True, default="")
    breed = models.ForeignKey(
        Breed, null=True, blank=True, on_delete=models.SET_NULL, related_name="animals"
    )
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default="Female")
    dob = models.DateField("Date of birth", null=True, blank=True)
    sire = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="offspring_sire",
    )
    dam = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="offspring_dam",
    )
    category = models.CharField(
        max_length=30, choices=CATEGORY_CHOICES, default="Heifer"
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Active")
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, default="Born")
    birth_weight = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    color = models.CharField(max_length=50, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tag_number} {self.name}".strip()

    def get_absolute_url(self):
        return reverse("herd:animal_detail", args=[self.pk])

    @property
    def full_name(self):
        return f"{self.tag_number} ({self.name})" if self.name else self.tag_number

    class Meta:
        ordering = ("tag_number",)
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["category"]),
        ]


class AnimalMovement(models.Model):
    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="movements"
    )
    movement_date = models.DateField()
    movement_type = models.CharField(
        max_length=30, choices=MOVEMENT_CHOICES, default="Barn Transfer"
    )
    from_location = models.CharField(max_length=100, blank=True, default="")
    to_location = models.CharField(max_length=100, blank=True, default="")
    reason = models.CharField(max_length=200, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal} — {self.movement_type} ({self.movement_date})"

    class Meta:
        ordering = ("-movement_date",)