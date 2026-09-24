"""Views for the employees module."""

from django.db.models import Sum
from django.urls import reverse_lazy

from core.views import AppCreateView, AppDeleteView, AppListView, AppUpdateView

from .forms import AdvanceForm, EmployeeForm, SalaryPaymentForm
from .models import Advance, Employee, SalaryPayment


class EmployeeListView(AppListView):
    model = Employee
    template_name = "employees/employee_list.html"
    context_object_name = "employees"
    title = "Employees"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_count"] = Employee.objects.filter(status="Active").count()
        ctx["monthly_payroll"] = (
            Employee.objects.filter(status="Active").aggregate(s=Sum("monthly_salary"))[
                "s"
            ]
            or 0
        )
        return ctx


class EmployeeAddView(AppCreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy("employees:employee_list")
    title = "Add Employee"
    cancel_url = reverse_lazy("employees:employee_list")
    success_message = "Employee added."


class EmployeeEditView(AppUpdateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy("employees:employee_list")
    title = "Edit Employee"
    cancel_url = reverse_lazy("employees:employee_list")
    success_message = "Employee updated."


class EmployeeDeleteView(AppDeleteView):
    model = Employee
    success_url = reverse_lazy("employees:employee_list")
    success_message = "Employee deleted."


class SalaryListView(AppListView):
    model = SalaryPayment
    template_name = "employees/salary_list.html"
    context_object_name = "payments"
    title = "Salary Payments"


class SalaryAddView(AppCreateView):
    model = SalaryPayment
    form_class = SalaryPaymentForm
    success_url = reverse_lazy("employees:salary_list")
    title = "Record Salary Payment"
    cancel_url = reverse_lazy("employees:salary_list")
    success_message = "Salary payment recorded."


class SalaryEditView(AppUpdateView):
    model = SalaryPayment
    form_class = SalaryPaymentForm
    success_url = reverse_lazy("employees:salary_list")
    title = "Edit Salary Payment"
    cancel_url = reverse_lazy("employees:salary_list")
    success_message = "Salary payment updated."


class SalaryDeleteView(AppDeleteView):
    model = SalaryPayment
    success_url = reverse_lazy("employees:salary_list")
    success_message = "Salary payment deleted."


class AdvanceListView(AppListView):
    model = Advance
    template_name = "employees/advance_list.html"
    context_object_name = "advances"
    title = "Salary Advances"


class AdvanceAddView(AppCreateView):
    model = Advance
    form_class = AdvanceForm
    success_url = reverse_lazy("employees:advance_list")
    title = "Record Advance"
    cancel_url = reverse_lazy("employees:advance_list")
    success_message = "Advance recorded."


class AdvanceEditView(AppUpdateView):
    model = Advance
    form_class = AdvanceForm
    success_url = reverse_lazy("employees:advance_list")
    title = "Edit Advance"
    cancel_url = reverse_lazy("employees:advance_list")
    success_message = "Advance updated."


class AdvanceDeleteView(AppDeleteView):
    model = Advance
    success_url = reverse_lazy("employees:advance_list")
    success_message = "Advance deleted."