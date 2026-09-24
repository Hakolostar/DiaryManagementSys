"""Admin configuration for the health module."""

from django.contrib import admin

from .models import Medicine, Treatment, Vaccination, VetVisit


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "stock_quantity", "unit_cost", "expiry_date")
    list_filter = ("category",)
    search_fields = ("name", "manufacturer")


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ("animal", "vaccine_name", "date", "next_due_date", "cost")
    search_fields = ("animal__tag_number", "animal__name", "vaccine_name")


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ("animal", "date", "diagnosis", "cost", "veterinarian")
    search_fields = ("animal__tag_number", "animal__name", "diagnosis")


@admin.register(VetVisit)
class VetVisitAdmin(admin.ModelAdmin):
    list_display = ("animal", "visit_date", "reason", "vet_name", "cost")
    search_fields = ("animal__tag_number", "animal__name", "reason")