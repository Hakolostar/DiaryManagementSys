"""Admin configuration for the breeding module."""

from django.contrib import admin

from .models import Calving, Heat, Insemination, Pregnancy


@admin.register(Heat)
class HeatAdmin(admin.ModelAdmin):
    list_display = ("animal", "heat_date", "expected_heat_date", "is_bred")
    list_filter = ("is_bred",)
    search_fields = ("animal__tag_number", "animal__name")


@admin.register(Insemination)
class InseminationAdmin(admin.ModelAdmin):
    list_display = (
        "animal",
        "service_date",
        "bull_name",
        "bull_breed",
        "cost",
        "result",
    )
    list_filter = ("result", "service_date")
    search_fields = ("animal__tag_number", "animal__name")


@admin.register(Pregnancy)
class PregnancyAdmin(admin.ModelAdmin):
    list_display = ("animal", "check_date", "diagnosis", "expected_calving_date")
    list_filter = ("diagnosis",)
    search_fields = ("animal__tag_number", "animal__name")


@admin.register(Calving)
class CalvingAdmin(admin.ModelAdmin):
    list_display = (
        "animal",
        "calving_date",
        "calving_type",
        "male_calves",
        "female_calves",
        "complication",
    )
    list_filter = ("calving_type", "complication")
    search_fields = ("animal__tag_number", "animal__name")