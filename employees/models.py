"""Employees module models: employees, salaries and advances."""

from django.db import models


class Employee(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("On Leave", "On Leave"),
        ("Resigned", "Resigned"),
        ("Terminated", "Terminated"),
    ]
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    employee_code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, default=""
    )
    phone = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    address = models.CharField(max_length=200, blank=True, default="")
    designation = models.CharField(max_length=100, blank=True, default="")
    department = models.CharField(max_length=100, blank=True, default="")
    hire_date = models.DateField(null=True, blank=True)
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Active")
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.name} ({self.employee_code})"

    class Meta:
        ordering = ("name",)


class SalaryPayment(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="salary_payments"
    )
    month = models.DateField(help_text="First day of the salary month")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")

    @property
    def net(self):
        return self.amount + self.bonus - self.deduction

    def __str__(self):
        return f"{self.employee.name} — {self.month:%b %Y}"

    class Meta:
        ordering = ("-month",)
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "month"], name="unique_salary_per_month"
            )
        ]


class Advance(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="advances"
    )
    advance_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    deduction_month = models.DateField(null=True, blank=True)
    repaid = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.employee.name} — advance {self.amount}"

    class Meta:
        ordering = ("-advance_date",)