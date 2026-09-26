"""URL routing for the invoicing module."""

from django.urls import path

from . import views

app_name = "invoicing"

urlpatterns = [
    path("", views.InvoiceListView.as_view(), name="invoice_list"),
    path("export/", views.invoice_export, name="invoice_export"),
    path("add/", views.InvoiceCreateView.as_view(), name="invoice_add"),
    path("<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice_detail"),
    path("<int:pk>/print/", views.InvoicePrintView.as_view(), name="invoice_print"),
    path("<int:pk>/edit/", views.InvoiceEditView.as_view(), name="invoice_edit"),
    path("<int:pk>/delete/", views.InvoiceDeleteView.as_view(), name="invoice_delete"),
]