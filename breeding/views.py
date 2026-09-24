"""Views for the breeding module — heat, AI, pregnancy and calving."""

from datetime import date, timedelta

from django.urls import reverse_lazy

from core.views import AppCreateView, AppDeleteView, AppListView, AppUpdateView

from .forms import CalvingForm, HeatForm, InseminationForm, PregnancyForm
from .models import Calving, Heat, Insemination, Pregnancy


class HeatListView(AppListView):
    model = Heat
    template_name = "breeding/heat_list.html"
    context_object_name = "heats"
    title = "Heat"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["due_heats"] = Heat.objects.filter(
            expected_heat_date__lte=date.today() + timedelta(days=7)
        ).select_related("animal")[:10]
        return ctx


class HeatAddView(AppCreateView):
    model = Heat
    form_class = HeatForm
    success_url = reverse_lazy("breeding:heat_list")
    title = "Record Heat"
    cancel_url = reverse_lazy("breeding:heat_list")
    success_message = "Heat recorded."


class HeatEditView(AppUpdateView):
    model = Heat
    form_class = HeatForm
    success_url = reverse_lazy("breeding:heat_list")
    title = "Edit Heat Record"
    cancel_url = reverse_lazy("breeding:heat_list")
    success_message = "Heat updated."


class HeatDeleteView(AppDeleteView):
    model = Heat
    success_url = reverse_lazy("breeding:heat_list")
    success_message = "Heat record deleted."


class InseminationListView(AppListView):
    model = Insemination
    template_name = "breeding/insemination_list.html"
    context_object_name = "records"
    title = "AI / Insemination"


class InseminationAddView(AppCreateView):
    model = Insemination
    form_class = InseminationForm
    success_url = reverse_lazy("breeding:insemination_list")
    title = "Record Insemination"
    cancel_url = reverse_lazy("breeding:insemination_list")
    success_message = "Insemination recorded."


class InseminationEditView(AppUpdateView):
    model = Insemination
    form_class = InseminationForm
    success_url = reverse_lazy("breeding:insemination_list")
    title = "Edit Insemination"
    cancel_url = reverse_lazy("breeding:insemination_list")
    success_message = "Insemination updated."


class InseminationDeleteView(AppDeleteView):
    model = Insemination
    success_url = reverse_lazy("breeding:insemination_list")
    success_message = "Insemination deleted."


class PregnancyListView(AppListView):
    model = Pregnancy
    template_name = "breeding/pregnancy_list.html"
    context_object_name = "pregnancies"
    title = "Pregnancy"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["due_calvings"] = Pregnancy.objects.filter(
            expected_calving_date__lte=date.today() + timedelta(days=14)
        ).select_related("animal")[:10]
        return ctx


class PregnancyAddView(AppCreateView):
    model = Pregnancy
    form_class = PregnancyForm
    success_url = reverse_lazy("breeding:pregnancy_list")
    title = "Record Pregnancy Check"
    cancel_url = reverse_lazy("breeding:pregnancy_list")
    success_message = "Pregnancy check recorded."


class PregnancyEditView(AppUpdateView):
    model = Pregnancy
    form_class = PregnancyForm
    success_url = reverse_lazy("breeding:pregnancy_list")
    title = "Edit Pregnancy Record"
    cancel_url = reverse_lazy("breeding:pregnancy_list")
    success_message = "Pregnancy record updated."


class PregnancyDeleteView(AppDeleteView):
    model = Pregnancy
    success_url = reverse_lazy("breeding:pregnancy_list")
    success_message = "Pregnancy record deleted."


class CalvingListView(AppListView):
    model = Calving
    template_name = "breeding/calving_list.html"
    context_object_name = "calvings"
    title = "Calving"


class CalvingAddView(AppCreateView):
    model = Calving
    form_class = CalvingForm
    success_url = reverse_lazy("breeding:calving_list")
    title = "Record Calving"
    cancel_url = reverse_lazy("breeding:calving_list")
    success_message = "Calving recorded."


class CalvingEditView(AppUpdateView):
    model = Calving
    form_class = CalvingForm
    success_url = reverse_lazy("breeding:calving_list")
    title = "Edit Calving Record"
    cancel_url = reverse_lazy("breeding:calving_list")
    success_message = "Calving updated."


class CalvingDeleteView(AppDeleteView):
    model = Calving
    success_url = reverse_lazy("breeding:calving_list")
    success_message = "Calving deleted."