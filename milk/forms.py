"""Forms for the milk module."""

from core.forms import StyledModelForm

from .models import Lactation, MilkProduction, MilkQuality, YieldTarget


class MilkProductionForm(StyledModelForm):
    class Meta:
        model = MilkProduction
        fields = ("animal", "date", "session", "quantity", "notes")


class LactationForm(StyledModelForm):
    class Meta:
        model = Lactation
        fields = (
            "animal",
            "lactation_number",
            "start_date",
            "dry_off_date",
            "expected_dry_off",
            "notes",
        )


class MilkQualityForm(StyledModelForm):
    class Meta:
        model = MilkQuality
        fields = (
            "animal",
            "date",
            "fat_pct",
            "protein_pct",
            "snf_pct",
            "density",
            "temperature",
            "remarks",
        )


class YieldTargetForm(StyledModelForm):
    class Meta:
        model = YieldTarget
        fields = ("animal", "target_daily_liters")