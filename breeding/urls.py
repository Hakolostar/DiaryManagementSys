"""URL routing for the breeding module."""

from django.urls import path

from . import views

app_name = "breeding"

urlpatterns = [
    # Heat
    path("heat/", views.HeatListView.as_view(), name="heat_list"),
    path("heat/add/", views.HeatAddView.as_view(), name="heat_add"),
    path("heat/<int:pk>/edit/", views.HeatEditView.as_view(), name="heat_edit"),
    path("heat/<int:pk>/delete/", views.HeatDeleteView.as_view(), name="heat_delete"),
    # AI / Insemination
    path(
        "insemination/",
        views.InseminationListView.as_view(),
        name="insemination_list",
    ),
    path(
        "insemination/add/",
        views.InseminationAddView.as_view(),
        name="insemination_add",
    ),
    path(
        "insemination/<int:pk>/edit/",
        views.InseminationEditView.as_view(),
        name="insemination_edit",
    ),
    path(
        "insemination/<int:pk>/delete/",
        views.InseminationDeleteView.as_view(),
        name="insemination_delete",
    ),
    # Pregnancy
    path("pregnancy/", views.PregnancyListView.as_view(), name="pregnancy_list"),
    path("pregnancy/add/", views.PregnancyAddView.as_view(), name="pregnancy_add"),
    path(
        "pregnancy/<int:pk>/edit/",
        views.PregnancyEditView.as_view(),
        name="pregnancy_edit",
    ),
    path(
        "pregnancy/<int:pk>/delete/",
        views.PregnancyDeleteView.as_view(),
        name="pregnancy_delete",
    ),
    # Calving
    path("calving/", views.CalvingListView.as_view(), name="calving_list"),
    path("calving/add/", views.CalvingAddView.as_view(), name="calving_add"),
    path(
        "calving/<int:pk>/edit/",
        views.CalvingEditView.as_view(),
        name="calving_edit",
    ),
    path(
        "calving/<int:pk>/delete/",
        views.CalvingDeleteView.as_view(),
        name="calving_delete",
    ),
]