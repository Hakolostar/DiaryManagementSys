"""URL routing for the herd module."""

from django.urls import path

from . import views

app_name = "herd"

urlpatterns = [
    # Animal Master
    path("", views.AnimalListView.as_view(), name="animal_list"),
    path("animals/table/", views.AnimalTableView.as_view(), name="animal_table"),
    path("animals/add/", views.AnimalAddView.as_view(), name="animal_add"),
    path("animals/<int:pk>/", views.AnimalDetailView.as_view(), name="animal_detail"),
    path("animals/<int:pk>/edit/", views.AnimalEditView.as_view(), name="animal_edit"),
    path(
        "animals/<int:pk>/delete/",
        views.AnimalDeleteView.as_view(),
        name="animal_delete",
    ),
    # Breeds
    path("breeds/", views.BreedListView.as_view(), name="breed_list"),
    path("breeds/add/", views.BreedAddView.as_view(), name="breed_add"),
    path("breeds/<int:pk>/edit/", views.BreedEditView.as_view(), name="breed_edit"),
    path(
        "breeds/<int:pk>/delete/",
        views.BreedDeleteView.as_view(),
        name="breed_delete",
    ),
    # Animal Movement
    path("movements/", views.MovementListView.as_view(), name="movement_list"),
    path("movements/add/", views.MovementAddView.as_view(), name="movement_add"),
    path(
        "movements/<int:pk>/delete/",
        views.MovementDeleteView.as_view(),
        name="movement_delete",
    ),
    # Animal History
    path("history/", views.HerdHistoryView.as_view(), name="history"),
]