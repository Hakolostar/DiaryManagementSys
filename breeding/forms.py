"""Forms for the breeding module."""

from core.forms import StyledModelForm

from .models import Calving, Heat, Insemination, Pregnancy


class HeatForm(StyledModelForm):
    class Meta:
        model = Heat
        fields = (
            "animal",
            "heat_date",
            "expected_heat_date",
            "is_bred",
            "detected_by",
            "notes",
        )


class InseminationForm(StyledModelForm):
    class Meta:
        model = Insemination
        fields = (
            "animal",
            "service_date",
            "bull_name",
            "bull_breed",
            "semen_source",
            "technician",
            "cost",
            "result",
            "notes",
        )


class PregnancyForm(StyledModelForm):
    class Meta:
        model = Pregnancy
        fields = (
            "animal",
            "insemination",
            "check_date",
            "diagnosis",
            "expected_calving_date",
            "confirmed_date",
            "notes",
        )


class CalvingForm(StyledModelForm):
    class Meta:
        model = Calving
        fields = (
            "animal",
            "calving_date",
            "calving_type",
            "male_calves",
            "female_calves",
            "complication",
            "vet_name",
            "notes",
        )