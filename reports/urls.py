"""URL routing for the reports module (dashboard + printable reports)."""

from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("reports/milk/", views.MilkReportView.as_view(), name="milk_report"),
    path("reports/herd/", views.HerdReportView.as_view(), name="herd_report"),
    path(
        "reports/breeding/",
        views.BreedingReportView.as_view(),
        name="breeding_report",
    ),
    path("reports/health/", views.HealthReportView.as_view(), name="health_report"),
    path("reports/feed/", views.FeedReportView.as_view(), name="feed_report"),
    path(
        "reports/finance/",
        views.FinanceReportView.as_view(),
        name="finance_report",
    ),
    path("reports/sales/", views.SalesReportView.as_view(), name="sales_report"),
    path(
        "reports/inventory/",
        views.InventoryReportView.as_view(),
        name="inventory_report",
    ),
]