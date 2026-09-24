"""URL routing for the employees module."""

from django.urls import path

from . import views

app_name = "employees"

urlpatterns = [
    path("", views.EmployeeListView.as_view(), name="employee_list"),
    path("add/", views.EmployeeAddView.as_view(), name="employee_add"),
    path("<int:pk>/edit/", views.EmployeeEditView.as_view(), name="employee_edit"),
    path("<int:pk>/delete/", views.EmployeeDeleteView.as_view(), name="employee_delete"),
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
]