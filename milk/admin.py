"""Admin configuration for the milk module."""

from django.contrib import admin

from .models import Lactation, MilkProduction, MilkQuality, YieldTarget


@admin.register(MilkProduction)
class MilkProductionAdmin(admin.ModelAdmin):
    list_display = ("animal", "date", "session", "quantity")
    list_filter = ("session", "date")
    search_fields = ("animal__tag_number", "animal__name")


@admin.register(Lactation)
class LactationAdmin(admin.ModelAdmin):
    list_display = ("animal", "lactation_number", "start_date", "dry_off_date")
    list_filter = ("start_date",)
    search_fields = ("animal__tag_number",)


@admin.register(MilkQuality)
class MilkQualityAdmin(admin.ModelAdmin):
    list_display = ("animal", "date", "fat_pct", "protein_pct", "snf_pct")
    search_fields = ("animal__tag_number", "animal__name")


@admin.register(YieldTarget)
class YieldTargetAdmin(admin.ModelAdmin):
    list_display = ("animal", "target_daily_liters")