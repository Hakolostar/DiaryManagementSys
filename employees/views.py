"""Views for the employees module — dashboard, directory, attendance, leave, claims."""

from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.views import AppCreateView, AppDeleteView, AppListView, AppMixin, AppUpdateView

from .forms import (
    AdvanceForm,
    AttendanceForm,
    EmployeeForm,
    ExpenseClaimForm,
    LeaveApplicationForm,
    SalaryPaymentForm,
)
from .models import (
    Advance,
    Attendance,
    Employee,
    ExpenseClaim,
    LeaveApplication,
    SalaryPayment,
)


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


class EmployeeDashboardView(AppMixin, TemplateView):
    template_name = "employees/dashboard.html"
    title = "Employee Dashboard"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_count"] = Employee.objects.filter(status="Active").count()
        ctx["monthly_payroll"] = Employee.objects.filter(
            status="Active"
        ).aggregate(s=Sum("monthly_salary"))["s"] or 0
        ctx["pending_leaves"] = LeaveApplication.objects.filter(
            status="Pending"
        ).count()
        ctx["pending_expenses"] = ExpenseClaim.objects.filter(status="Pending").count()
        ctx["today_present"] = Attendance.objects.filter(
            date=date.today(), status="Present"
        ).count()
        ctx["today_absent"] = Attendance.objects.filter(
            date=date.today(), status="Absent"
        ).count()
        ctx["headcount_by_dept"] = list(
            Employee.objects.values("department")
            .annotate(n=Count("id"))
            .order_by("-n")[:6]
        )
        return ctx


class AttendanceListView(AppListView):
    model = Attendance
    template_name = "employees/attendance_list.html"
    context_object_name = "records"
    title = "Attendance Tracking"


class AttendanceAddView(AppCreateView):
    model = Attendance
    form_class = AttendanceForm
    success_url = reverse_lazy("employees:attendance_list")
    title = "Mark Attendance"
    cancel_url = reverse_lazy("employees:attendance_list")
    success_message = "Attendance marked."


class AttendanceEditView(AppUpdateView):
    model = Attendance
    form_class = AttendanceForm
    success_url = reverse_lazy("employees:attendance_list")
    title = "Edit Attendance"
    cancel_url = reverse_lazy("employees:attendance_list")
    success_message = "Attendance updated."


class AttendanceDeleteView(AppDeleteView):
    model = Attendance
    success_url = reverse_lazy("employees:attendance_list")
    success_message = "Attendance record deleted."


class LeaveListView(AppListView):
    model = LeaveApplication
    template_name = "employees/leave_list.html"
    context_object_name = "leaves"
    title = "Leave Applications"


class LeaveAddView(AppCreateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    success_url = reverse_lazy("employees:leave_list")
    title = "Apply for Leave"
    cancel_url = reverse_lazy("employees:leave_list")
    success_message = "Leave application submitted."


class LeaveEditView(AppUpdateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    success_url = reverse_lazy("employees:leave_list")
    title = "Edit Leave Application"
    cancel_url = reverse_lazy("employees:leave_list")
    success_message = "Leave application updated."


class LeaveDeleteView(AppDeleteView):
    model = LeaveApplication
    success_url = reverse_lazy("employees:leave_list")
    success_message = "Leave application deleted."


class ExpenseClaimListView(AppListView):
    model = ExpenseClaim
    template_name = "employees/expense_list.html"
    context_object_name = "claims"
    title = "Expense Claims"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["pending_total"] = sum(
            float(c.amount)
            for c in ExpenseClaim.objects.filter(status__in=["Pending", "Approved"])
        )
        return ctx


class ExpenseClaimAddView(AppCreateView):
    model = ExpenseClaim
    form_class = ExpenseClaimForm
    success_url = reverse_lazy("employees:expense_list")
    title = "Submit Expense Claim"
    cancel_url = reverse_lazy("employees:expense_list")
    success_message = "Expense claim submitted."


class ExpenseClaimEditView(AppUpdateView):
    model = ExpenseClaim
    form_class = ExpenseClaimForm
    success_url = reverse_lazy("employees:expense_list")
    title = "Edit Expense Claim"
    cancel_url = reverse_lazy("employees:expense_list")
    success_message = "Expense claim updated."


class ExpenseClaimDeleteView(AppDeleteView):
    model = ExpenseClaim
    success_url = reverse_lazy("employees:expense_list")
    success_message = "Expense claim deleted."


class HRReportsView(AppMixin, TemplateView):
    template_name = "employees/hr_reports.html"
    title = "HR Reports"

    def get(self, request, *args, **kwargs):
        """Serve an Excel headcount sheet when ``?format=xlsx`` is requested."""
        if request.GET.get("format") == "xlsx":
            from core.xlsx import build_xlsx_response

            ctx = self.get_context_data()
            headers = ["Department", "Staff count"]
            rows = [
                [d["department"] or "Unassigned", d["n"]]
                for d in ctx["headcount_by_dept"]
            ]
            return build_xlsx_response("hr_headcount_report", headers, rows)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["request"] = self.request
        ctx["headcount_by_dept"] = list(
            Employee.objects.values("department")
            .annotate(n=Count("id"))
            .order_by("-n")
        )
        ctx["headcount_by_status"] = list(
            Employee.objects.values("status")
            .annotate(n=Count("id"))
            .order_by("status")
        )
        ctx["salary_total"] = Employee.objects.filter(status="Active").aggregate(
            s=Sum("monthly_salary")
        )["s"] or 0
        ctx["attendance_summary"] = list(
            Attendance.objects.values("status")
            .annotate(n=Count("id"))
            .order_by("status")
        )
        ctx["approved_leaves"] = list(
            LeaveApplication.objects.select_related("employee").filter(
                status="Approved"
            )[:30]
        )
        ctx["claims_amount"] = ExpenseClaim.objects.filter(
            status__in=["Pending", "Approved"]
        ).aggregate(s=Sum("amount"))["s"] or 0
        return ctx


@login_required
def employee_export(request):
    """Export the employee directory to an .xlsx file."""
    from core.xlsx import build_xlsx_response

    employees = Employee.objects.all()
    headers = [
        "Code", "Name", "Gender", "Designation", "Department", "Phone",
        "Email", "Hire Date", "Monthly Salary", "Status",
    ]
    rows = [
        [
            e.employee_code, e.name, e.gender, e.designation, e.department,
            e.phone, e.email, e.hire_date, float(e.monthly_salary), e.status,
        ]
        for e in employees
    ]
    return build_xlsx_response("employees", headers, rows)