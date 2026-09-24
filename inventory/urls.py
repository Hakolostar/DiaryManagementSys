"""URL routing for the inventory module."""

from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.InventoryListView.as_view(), name="item_list"),
    path("items/add/", views.InventoryAddView.as_view(), name="item_add"),
    path("items/<int:pk>/edit/", views.InventoryEditView.as_view(), name="item_edit"),
    path(
        "items/<int:pk>/delete/",
        views.InventoryDeleteView.as_view(),
        name="item_delete",
    ),
    path(
        "movements/",
        views.TransactionListView.as_view(),
        name="transaction_list",
    ),
    path(
        "movements/add/",
        views.TransactionAddView.as_view(),
        name="transaction_add",
    ),
    path(
        "movements/<int:pk>/delete/",
        views.TransactionDeleteView.as_view(),
        name="transaction_delete",
    ),
]