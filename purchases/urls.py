"""URL routing for the purchases module."""

from django.urls import path

from . import views

app_name = "purchases"

urlpatterns = [
    path("", views.PurchaseListView.as_view(), name="purchase_list"),
    path("add/", views.PurchaseAddView.as_view(), name="purchase_add"),
    path("<int:pk>/edit/", views.PurchaseEditView.as_view(), name="purchase_edit"),
    path(
        "<int:pk>/delete/",
        views.PurchaseDeleteView.as_view(),
        name="purchase_delete",
    ),
    path("suppliers/", views.SupplierListView.as_view(), name="supplier_list"),
    path("suppliers/add/", views.SupplierAddView.as_view(), name="supplier_add"),
    path(
        "suppliers/<int:pk>/edit/",
        views.SupplierEditView.as_view(),
        name="supplier_edit",
    ),
    path(
        "suppliers/<int:pk>/delete/",
        views.SupplierDeleteView.as_view(),
        name="supplier_delete",
    ),
]