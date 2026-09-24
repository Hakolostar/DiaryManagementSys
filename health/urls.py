"""URL routing for the health module."""

from django.urls import path

from . import views

app_name = "health"

urlpatterns = [
    # Medicine
    path("medicine/", views.MedicineListView.as_view(), name="medicine_list"),
    path("medicine/add/", views.MedicineAddView.as_view(), name="medicine_add"),
    path(
        "medicine/<int:pk>/edit/",
        views.MedicineEditView.as_view(),
        name="medicine_edit",
    ),
    path(
        "medicine/<int:pk>/delete/",
        views.MedicineDeleteView.as_view(),
        name="medicine_delete",
    ),
    # Vaccination
    path(
        "vaccination/",
        views.VaccinationListView.as_view(),
        name="vaccination_list",
    ),
    path(
        "vaccination/add/",
        views.VaccinationAddView.as_view(),
        name="vaccination_add",
    ),
    path(
        "vaccination/<int:pk>/edit/",
        views.VaccinationEditView.as_view(),
        name="vaccination_edit",
    ),
    path(
        "vaccination/<int:pk>/delete/",
        views.VaccinationDeleteView.as_view(),
        name="vaccination_delete",
    ),
    # Treatment
    path("treatment/", views.TreatmentListView.as_view(), name="treatment_list"),
    path("treatment/add/", views.TreatmentAddView.as_view(), name="treatment_add"),
    path(
        "treatment/<int:pk>/edit/",
        views.TreatmentEditView.as_view(),
        name="treatment_edit",
    ),
    path(
        "treatment/<int:pk>/delete/",
        views.TreatmentDeleteView.as_view(),
        name="treatment_delete",
    ),
    # Vet visits
    path("vet-visits/", views.VetVisitListView.as_view(), name="vet_visit_list"),
    path("vet-visits/add/", views.VetVisitAddView.as_view(), name="vet_visit_add"),
    path(
        "vet-visits/<int:pk>/edit/",
        views.VetVisitEditView.as_view(),
        name="vet_visit_edit",
    ),
    path(
        "vet-visits/<int:pk>/delete/",
        views.VetVisitDeleteView.as_view(),
        name="vet_visit_delete",
    ),
]