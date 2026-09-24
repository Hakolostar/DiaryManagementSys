"""Views for the health module — medicine, vaccination, treatment, vet visits."""

from datetime import date, timedelta

from django.urls import reverse_lazy

from core.views import AppCreateView, AppDeleteView, AppListView, AppUpdateView

from .forms import MedicineForm, TreatmentForm, VaccinationForm, VetVisitForm
from .models import Medicine, Treatment, Vaccination, VetVisit


class MedicineListView(AppListView):
    model = Medicine
    template_name = "health/medicine_list.html"
    context_object_name = "medicines"
    title = "Medicine"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["low_stock"] = [m for m in Medicine.objects.all() if m.is_low]
        return ctx


class MedicineAddView(AppCreateView):
    model = Medicine
    form_class = MedicineForm
    success_url = reverse_lazy("health:medicine_list")
    title = "Add Medicine"
    cancel_url = reverse_lazy("health:medicine_list")
    success_message = "Medicine added."


class MedicineEditView(AppUpdateView):
    model = Medicine
    form_class = MedicineForm
    success_url = reverse_lazy("health:medicine_list")
    title = "Edit Medicine"
    cancel_url = reverse_lazy("health:medicine_list")
    success_message = "Medicine updated."


class MedicineDeleteView(AppDeleteView):
    model = Medicine
    success_url = reverse_lazy("health:medicine_list")
    success_message = "Medicine deleted."


class VaccinationListView(AppListView):
    model = Vaccination
    template_name = "health/vaccination_list.html"
    context_object_name = "vaccinations"
    title = "Vaccination"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["due_vaccinations"] = Vaccination.objects.filter(
            next_due_date__lte=date.today() + timedelta(days=30)
        ).select_related("animal")[:10]
        return ctx


class VaccinationAddView(AppCreateView):
    model = Vaccination
    form_class = VaccinationForm
    success_url = reverse_lazy("health:vaccination_list")
    title = "Record Vaccination"
    cancel_url = reverse_lazy("health:vaccination_list")
    success_message = "Vaccination recorded."


class VaccinationEditView(AppUpdateView):
    model = Vaccination
    form_class = VaccinationForm
    success_url = reverse_lazy("health:vaccination_list")
    title = "Edit Vaccination"
    cancel_url = reverse_lazy("health:vaccination_list")
    success_message = "Vaccination updated."


class VaccinationDeleteView(AppDeleteView):
    model = Vaccination
    success_url = reverse_lazy("health:vaccination_list")
    success_message = "Vaccination deleted."


class TreatmentListView(AppListView):
    model = Treatment
    template_name = "health/treatment_list.html"
    context_object_name = "treatments"
    title = "Treatment"


class TreatmentAddView(AppCreateView):
    model = Treatment
    form_class = TreatmentForm
    success_url = reverse_lazy("health:treatment_list")
    title = "Record Treatment"
    cancel_url = reverse_lazy("health:treatment_list")
    success_message = "Treatment recorded."


class TreatmentEditView(AppUpdateView):
    model = Treatment
    form_class = TreatmentForm
    success_url = reverse_lazy("health:treatment_list")
    title = "Edit Treatment"
    cancel_url = reverse_lazy("health:treatment_list")
    success_message = "Treatment updated."


class TreatmentDeleteView(AppDeleteView):
    model = Treatment
    success_url = reverse_lazy("health:treatment_list")
    success_message = "Treatment deleted."


class VetVisitListView(AppListView):
    model = VetVisit
    template_name = "health/vet_visit_list.html"
    context_object_name = "visits"
    title = "Veterinary Visits"


class VetVisitAddView(AppCreateView):
    model = VetVisit
    form_class = VetVisitForm
    success_url = reverse_lazy("health:vet_visit_list")
    title = "Record Vet Visit"
    cancel_url = reverse_lazy("health:vet_visit_list")
    success_message = "Vet visit recorded."


class VetVisitEditView(AppUpdateView):
    model = VetVisit
    form_class = VetVisitForm
    success_url = reverse_lazy("health:vet_visit_list")
    title = "Edit Vet Visit"
    cancel_url = reverse_lazy("health:vet_visit_list")
    success_message = "Vet visit updated."


class VetVisitDeleteView(AppDeleteView):
    model = VetVisit
    success_url = reverse_lazy("health:vet_visit_list")
    success_message = "Vet visit deleted."