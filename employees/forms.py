"""Forms for the employees module."""

from core.forms import StyledModelForm

from .models import Advance, Employee, SalaryPayment


class EmployeeForm(StyledModelForm):
    class Meta:
        model = Employee
        fields = (
            "employee_code",
            "name",
            "gender",
            "phone",
            "email",
            "address",
            "designation",
            "department",
            "hire_date",
            "monthly_salary",
            "status",
            "notes",
        )


class SalaryPaymentForm(StyledModelForm):
    class Meta:
        model = SalaryPayment
        fields = ("employee", "month", "amount", "bonus", "deduction", "paid_date", "notes")


class AdvanceForm(StyledModelForm):
    class Meta:
        model = Advance
        fields = ("employee", "advance_date", "amount", "deduction_month", "repaid", "notes")