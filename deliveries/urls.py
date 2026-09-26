"""URL routing for the deliveries module."""

from django.urls import path

from . import views

app_name = "deliveries"

urlpatterns = [
    path("", views.DeliveryNoteListView.as_view(), name="delivery_note_list"),
    path("export/", views.delivery_note_export, name="delivery_note_export"),
    path("add/", views.DeliveryNoteCreateView.as_view(), name="delivery_note_add"),
    path(
        "<int:pk>/",
        views.DeliveryNoteDetailView.as_view(),
        name="delivery_note_detail",
    ),
    path(
        "<int:pk>/print/",
        views.DeliveryNotePrintView.as_view(),
        name="delivery_note_print",
    ),
    path(
        "<int:pk>/edit/",
        views.DeliveryNoteEditView.as_view(),
        name="delivery_note_edit",
    ),
    path(
        "<int:pk>/delete/",
        views.DeliveryNoteDeleteView.as_view(),
        name="delivery_note_delete",
    ),
]