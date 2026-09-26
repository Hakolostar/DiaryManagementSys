"""Admin configuration for the employees module."""

from django.contrib import admin

from .models import (
    Advance,
    Attendance,
    Employee,
    ExpenseClaim,
    LeaveApplication,
    SalaryPayment,
)


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


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "status")
    list_filter = ("status", "date")
    search_fields = ("employee__name", "employee__employee_code")


@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ("employee", "leave_type", "start_date", "end_date", "status")
    list_filter = ("status", "leave_type")
    search_fields = ("employee__name",)


@admin.register(ExpenseClaim)
class ExpenseClaimAdmin(admin.ModelAdmin):
    list_display = ("employee", "claim_date", "category", "amount", "status")
    list_filter = ("status", "category")
    search_fields = ("employee__name", "description")