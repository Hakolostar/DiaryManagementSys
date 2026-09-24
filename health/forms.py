"""Forms for the health module."""

from core.forms import StyledModelForm

from .models import Medicine, Treatment, Vaccination, VetVisit


class MedicineForm(StyledModelForm):
    class Meta:
        model = Medicine
        fields = (
            "name",
            "category",
            "manufacturer",
            "unit",
            "stock_quantity",
            "unit_cost",
            "expiry_date",
            "reorder_level",
            "notes",
        )


class VaccinationForm(StyledModelForm):
    class Meta:
        model = Vaccination
        fields = (
            "animal",
            "vaccine_name",
            "date",
            "next_due_date",
            "dosage",
            "administered_by",
            "cost",
            "notes",
        )


class TreatmentForm(StyledModelForm):
    class Meta:
        model = Treatment
        fields = (
            "animal",
            "date",
            "diagnosis",
            "treatment_applied",
            "medicines",
            "cost",
            "veterinarian",
            "notes",
        )


class VetVisitForm(StyledModelForm):
    class Meta:
        model = VetVisit
        fields = (
            "animal",
            "visit_date",
            "reason",
            "findings",
            "treatment_applied",
            "vet_name",
            "follow_up_date",
            "cost",
            "notes",
        )