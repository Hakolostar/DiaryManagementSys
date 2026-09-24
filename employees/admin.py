"""Admin configuration for the employees module."""

from django.contrib import admin

from .models import Advance, Employee, SalaryPayment


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_code",
        "name",
        "designation",
        "department",
        "monthly_salary",
        "status",
    )
    list_filter = ("status", "department")
    search_fields = ("name", "employee_code", "phone")


@admin.register(SalaryPayment)
class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ("employee", "month", "amount", "bonus", "deduction", "net", "paid_date")
    list_filter = ("month",)
    search_fields = ("employee__name", "employee__employee_code")


@admin.register(Advance)
class AdvanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "advance_date", "amount", "deduction_month", "repaid")
    list_filter = ("repaid",)
    search_fields = ("employee__name",)