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


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Half Day", "Half Day"),
        ("Leave", "Leave"),
    ]
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="attendance"
    )
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Present")
    notes = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return f"{self.employee.name} — {self.status} ({self.date})"

    class Meta:
        ordering = ("-date",)
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "date"], name="unique_attendance_per_day"
            )
        ]


class LeaveApplication(models.Model):
    LEAVE_TYPE_CHOICES = [
        ("Annual", "Annual"),
        ("Sick", "Sick"),
        ("Maternity", "Maternity"),
        ("Casual", "Casual"),
        ("Unpaid", "Unpaid"),
    ]
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="leave_applications"
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, default="Casual")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    reason = models.TextField(blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    approved_by = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def days(self):
        if not self.end_date:
            return 1
        return max((self.end_date - self.start_date).days + 1, 1)

    def __str__(self):
        return f"{self.employee.name} — {self.leave_type} leave"

    class Meta:
        ordering = ("-start_date",)


class ExpenseClaim(models.Model):
    CATEGORY_CHOICES = [
        ("Transport", "Transport"),
        ("Meals", "Meals"),
        ("Travel", "Travel"),
        ("Medical", "Medical"),
        ("Other", "Other"),
    ]
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Paid", "Paid"),
    ]
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="expense_claims"
    )
    claim_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="Other")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=200, blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} — {self.category} {self.amount}"

    class Meta:
        ordering = ("-claim_date",)