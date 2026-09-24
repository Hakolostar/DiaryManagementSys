"""URL routing for the milk module."""

from django.urls import path

from . import views

app_name = "milk"

urlpatterns = [
    # Morning milk
    path(
        "morning/",
        views.MilkProductionListView.as_view(session="Morning"),
        name="morning_milk",
    ),
    path(
        "morning/add/",
        views.MilkProductionAddView.as_view(session="Morning"),
        name="morning_milk_add",
    ),
    # Evening milk
    path(
        "evening/",
        views.MilkProductionListView.as_view(session="Evening"),
        name="evening_milk",
    ),
    path(
        "evening/add/",
        views.MilkProductionAddView.as_view(session="Evening"),
        name="evening_milk_add",
    ),
    path(
        "records/<int:pk>/edit/",
        views.MilkProductionEditView.as_view(),
        name="milk_edit",
    ),
    path(
        "records/<int:pk>/delete/",
        views.MilkProductionDeleteView.as_view(),
        name="milk_delete",
    ),
    # Cow yield
    path("yield/", views.CowYieldView.as_view(), name="cow_yield"),
    path(
        "yield/targets/",
        views.YieldTargetListView.as_view(),
        name="yield_target_list",
    ),
    path(
        "yield/targets/add/",
        views.YieldTargetAddView.as_view(),
        name="yield_target_add",
    ),
    path(
        "yield/targets/<int:pk>/edit/",
        views.YieldTargetEditView.as_view(),
        name="yield_target_edit",
    ),
    # Lactation
    path("lactations/", views.LactationListView.as_view(), name="lactation_list"),
    path("lactations/add/", views.LactationAddView.as_view(), name="lactation_add"),
    path(
        "lactations/<int:pk>/edit/",
        views.LactationEditView.as_view(),
        name="lactation_edit",
    ),
    path(
        "lactations/<int:pk>/delete/",
        views.LactationDeleteView.as_view(),
        name="lactation_delete",
    ),
    # Milk quality
    path("quality/", views.QualityListView.as_view(), name="quality_list"),
    path("quality/add/", views.QualityAddView.as_view(), name="quality_add"),
    path(
        "quality/<int:pk>/edit/",
        views.QualityEditView.as_view(),
        name="quality_edit",
    ),
    path(
        "quality/<int:pk>/delete/",
        views.QualityDeleteView.as_view(),
        name="quality_delete",
    ),
]