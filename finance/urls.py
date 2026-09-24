"""URL routing for the finance module."""

from django.urls import path

from . import views

app_name = "finance"

urlpatterns = [
    path("", views.TransactionListView.as_view(), name="transaction_list"),
    path("transactions/add/", views.TransactionAddView.as_view(), name="transaction_add"),
    path(
        "transactions/<int:pk>/edit/",
        views.TransactionEditView.as_view(),
        name="transaction_edit",
    ),
    path(
        "transactions/<int:pk>/delete/",
        views.TransactionDeleteView.as_view(),
        name="transaction_delete",
    ),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("categories/add/", views.CategoryAddView.as_view(), name="category_add"),
    path(
        "categories/<int:pk>/edit/",
        views.CategoryEditView.as_view(),
        name="category_edit",
    ),
    path(
        "categories/<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category_delete",
    ),
]