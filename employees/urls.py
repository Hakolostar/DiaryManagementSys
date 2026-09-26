"""URL routing for the employees module."""

from django.urls import path

from . import views

app_name = "employees"

urlpatterns = [
    # Grid dashboard (home of the module)
    path("", views.EmployeeDashboardView.as_view(), name="dashboard"),
    # Directory
    path("directory/", views.EmployeeListView.as_view(), name="employee_list"),
    path("directory/add/", views.EmployeeAddView.as_view(), name="employee_add"),
    path(
        "directory/<int:pk>/edit/",
        views.EmployeeEditView.as_view(),
        name="employee_edit",
    ),
    path(
        "directory/<int:pk>/delete/",
        views.EmployeeDeleteView.as_view(),
        name="employee_delete",
    ),
    path("directory/export/", views.employee_export, name="employee_export"),
    # Payroll / Allowances
    path("salaries/", views.SalaryListView.as_view(), name="salary_list"),
    path("salaries/add/", views.SalaryAddView.as_view(), name="salary_add"),
    path(
        "salaries/<int:pk>/edit/",
        views.SalaryEditView.as_view(),
        name="salary_edit",
    ),
    path(
        "salaries/<int:pk>/delete/",
        views.SalaryDeleteView.as_view(),
        name="salary_delete",
    ),
    path("advances/", views.AdvanceListView.as_view(), name="advance_list"),
    path("advances/add/", views.AdvanceAddView.as_view(), name="advance_add"),
    path(
        "advances/<int:pk>/edit/",
        views.AdvanceEditView.as_view(),
        name="advance_edit",
    ),
    path(
        "advances/<int:pk>/delete/",
        views.AdvanceDeleteView.as_view(),
        name="advance_delete",
    ),
    # Attendance
    path("attendance/", views.AttendanceListView.as_view(), name="attendance_list"),
    path("attendance/add/", views.AttendanceAddView.as_view(), name="attendance_add"),
    path(
        "attendance/<int:pk>/edit/",
        views.AttendanceEditView.as_view(),
        name="attendance_edit",
    ),
    path(
        "attendance/<int:pk>/delete/",
        views.AttendanceDeleteView.as_view(),
        name="attendance_delete",
    ),
    # Leave applications
    path("leave/", views.LeaveListView.as_view(), name="leave_list"),
    path("leave/add/", views.LeaveAddView.as_view(), name="leave_add"),
    path("leave/<int:pk>/edit/", views.LeaveEditView.as_view(), name="leave_edit"),
    path(
        "leave/<int:pk>/delete/",
        views.LeaveDeleteView.as_view(),
        name="leave_delete",
    ),
    # Expense claims
    path("expenses/", views.ExpenseClaimListView.as_view(), name="expense_list"),
    path("expenses/add/", views.ExpenseClaimAddView.as_view(), name="expense_add"),
    path(
        "expenses/<int:pk>/edit/",
        views.ExpenseClaimEditView.as_view(),
        name="expense_edit",
    ),
    path(
        "expenses/<int:pk>/delete/",
        views.ExpenseClaimDeleteView.as_view(),
        name="expense_delete",
    ),
    # HR reports
    path("reports/", views.HRReportsView.as_view(), name="hr_reports"),
]