"""URL routing for the feed module."""

from django.urls import path

from . import views

app_name = "feed"

urlpatterns = [
    # Feed items
    path("items/", views.FeedItemListView.as_view(), name="item_list"),
    path("items/add/", views.FeedItemAddView.as_view(), name="item_add"),
    path("items/<int:pk>/edit/", views.FeedItemEditView.as_view(), name="item_edit"),
    path(
        "items/<int:pk>/delete/",
        views.FeedItemDeleteView.as_view(),
        name="item_delete",
    ),
    # Feed consumption
    path(
        "consumption/",
        views.ConsumptionListView.as_view(),
        name="consumption_list",
    ),
    path(
        "consumption/add/",
        views.ConsumptionAddView.as_view(),
        name="consumption_add",
    ),
    path(
        "consumption/<int:pk>/edit/",
        views.ConsumptionEditView.as_view(),
        name="consumption_edit",
    ),
    path(
        "consumption/<int:pk>/delete/",
        views.ConsumptionDeleteView.as_view(),
        name="consumption_delete",
    ),
    # Feed purchase
    path("purchases/", views.PurchaseListView.as_view(), name="purchase_list"),
    path("purchases/add/", views.PurchaseAddView.as_view(), name="purchase_add"),
    path(
        "purchases/<int:pk>/edit/",
        views.PurchaseEditView.as_view(),
        name="purchase_edit",
    ),
    path(
        "purchases/<int:pk>/delete/",
        views.PurchaseDeleteView.as_view(),
        name="purchase_delete",
    ),
    # Feed cost report
    path("cost/", views.FeedCostView.as_view(), name="feed_cost"),
]