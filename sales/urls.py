"""URL routing for the sales module."""

from django.urls import path

from . import views

app_name = "sales"

urlpatterns = [
    path("", views.SaleListView.as_view(), name="sale_list"),
    path("add/", views.SaleAddView.as_view(), name="sale_add"),
    path("<int:pk>/edit/", views.SaleEditView.as_view(), name="sale_edit"),
    path("<int:pk>/delete/", views.SaleDeleteView.as_view(), name="sale_delete"),
    path("customers/", views.CustomerListView.as_view(), name="customer_list"),
    path("customers/add/", views.CustomerAddView.as_view(), name="customer_add"),
    path(
        "customers/<int:pk>/edit/",
        views.CustomerEditView.as_view(),
        name="customer_edit",
    ),
    path(
        "customers/<int:pk>/delete/",
        views.CustomerDeleteView.as_view(),
        name="customer_delete",
    ),
]