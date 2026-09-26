"""Views for the milk module — Morning/Evening milk, yield, lactation, quality."""

from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.views import AppCreateView, AppDeleteView, AppListView, AppMixin, AppUpdateView
from herd.models import Animal

from .forms import LactationForm, MilkProductionForm, MilkQualityForm, YieldTargetForm
from .models import Lactation, MilkProduction, MilkQuality, YieldTarget


class MilkProductionListView(AppListView):
    model = MilkProduction
    template_name = "milk/milk_list.html"
    context_object_name = "records"
    session = "Morning"

    def get_queryset(self):
        qs = MilkProduction.objects.select_related("animal").filter(
            session=self.session
        )
        d = self.request.GET.get("date", "")
        animal = self.request.GET.get("animal", "")
        if d:
            qs = qs.filter(date=d)
        if animal:
            qs = qs.filter(animal__tag_number__icontains=animal)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_session"] = self.session
        ctx["title"] = f"{self.session} Milk"
        ctx["date"] = self.request.GET.get("date", "")
        ctx["total"] = self.get_queryset().aggregate(s=Sum("quantity"))["s"] or 0
        return ctx


class MilkProductionAddView(AppCreateView):
    model = MilkProduction
    form_class = MilkProductionForm
    session = "Morning"
    success_message = "Milk quantity recorded."

    def get_initial(self):
        initial = super().get_initial()
        initial["session"] = self.session
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = f"Record {self.session} Milk"
        ctx["cancel_url"] = self.get_success_url()
        return ctx

    def get_success_url(self):
        name = "milk:evening_milk" if self.session == "Evening" else "milk:morning_milk"
        return reverse_lazy(name)

    def form_valid(self, form):
        form.instance.session = self.session
        return super().form_valid(form)


class MilkProductionEditView(AppUpdateView):
    model = MilkProduction
    form_class = MilkProductionForm
    success_url = reverse_lazy("milk:morning_milk")
    title = "Edit Milk Record"
    cancel_url = reverse_lazy("milk:morning_milk")
    success_message = "Milk record updated."


class MilkProductionDeleteView(AppDeleteView):
    model = MilkProduction
    success_url = reverse_lazy("milk:morning_milk")
    success_message = "Milk record deleted."


class CowYieldView(AppMixin, TemplateView):
    template_name = "milk/cow_yield.html"
    title = "Cow Yield"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        month_start = today.replace(day=1)
        rows = []
        for animal in (
            Animal.objects.filter(status="Active", sex="Female")
            .prefetch_related("milk_records")
            .select_related("breed")
        ):
            recs = animal.milk_records.all()
            month_recs = [r for r in recs if r.date >= month_start]
            month_total = sum(r.quantity for r in month_recs)
            month_days = len({r.date for r in month_recs})
            lifetime = sum(r.quantity for r in recs)
            target = getattr(animal, "yield_target", None)
            rows.append(
                {
                    "animal": animal,
                    "month_total": month_total,
                    "days_milked": month_days,
                    "avg_per_day": round(month_total / month_days, 2)
                    if month_days
                    else 0,
                    "lifetime_total": lifetime,
                    "target": target.target_daily_liters if target else 0,
                }
            )
        rows.sort(key=lambda r: r["month_total"], reverse=True)
        ctx["rows"] = rows
        ctx["month"] = today.strftime("%B %Y")
        return ctx


class LactationListView(AppListView):
    model = Lactation
    template_name = "milk/lactation_list.html"
    context_object_name = "lactations"
    title = "Lactation"

    def get_queryset(self):
        return Lactation.objects.select_related("animal").all()


class LactationAddView(AppCreateView):
    model = Lactation
    form_class = LactationForm
    success_url = reverse_lazy("milk:lactation_list")
    title = "Add Lactation"
    cancel_url = reverse_lazy("milk:lactation_list")
    success_message = "Lactation added."


class LactationEditView(AppUpdateView):
    model = Lactation
    form_class = LactationForm
    success_url = reverse_lazy("milk:lactation_list")
    title = "Edit Lactation"
    cancel_url = reverse_lazy("milk:lactation_list")
    success_message = "Lactation updated."


class LactationDeleteView(AppDeleteView):
    model = Lactation
    success_url = reverse_lazy("milk:lactation_list")
    success_message = "Lactation deleted."


class QualityListView(AppListView):
    model = MilkQuality
    template_name = "milk/quality_list.html"
    context_object_name = "qualities"
    title = "Milk Quality"


class QualityAddView(AppCreateView):
    model = MilkQuality
    form_class = MilkQualityForm
    success_url = reverse_lazy("milk:quality_list")
    title = "Record Milk Quality"
    cancel_url = reverse_lazy("milk:quality_list")
    success_message = "Quality record saved."


class QualityEditView(AppUpdateView):
    model = MilkQuality
    form_class = MilkQualityForm
    success_url = reverse_lazy("milk:quality_list")
    title = "Edit Quality Record"
    cancel_url = reverse_lazy("milk:quality_list")
    success_message = "Quality record updated."


class QualityDeleteView(AppDeleteView):
    model = MilkQuality
    success_url = reverse_lazy("milk:quality_list")
    success_message = "Quality record deleted."


class YieldTargetListView(AppListView):
    model = YieldTarget
    template_name = "milk/yield_target_list.html"
    context_object_name = "targets"
    title = "Yield Targets"

    def get_queryset(self):
        return YieldTarget.objects.select_related("animal").order_by(
            "animal__tag_number"
        )


class YieldTargetAddView(AppCreateView):
    model = YieldTarget
    form_class = YieldTargetForm
    success_url = reverse_lazy("milk:yield_target_list")
    title = "Set Yield Target"
    cancel_url = reverse_lazy("milk:yield_target_list")
    success_message = "Yield target set."


class YieldTargetEditView(AppUpdateView):
    model = YieldTarget
    form_class = YieldTargetForm
    success_url = reverse_lazy("milk:yield_target_list")
    title = "Edit Yield Target"
    cancel_url = reverse_lazy("milk:yield_target_list")
    success_message = "Yield target updated."


@login_required
def milk_export(request):
    """Export a daily morning/evening milk summary to an .xlsx file."""
    from django.db.models import Count

    from core.xlsx import build_xlsx_response

    qs = (
        MilkProduction.objects.values("date", "session")
        .annotate(total=Sum("quantity"), n=Count("id"))
        .order_by("-date")
    )
    headers = ["Date", "Session", "Total (litres)", "Record Count"]
    rows = [
        [r["date"], r["session"], float(r["total"]), r["n"]]
        for r in qs
    ]
    return build_xlsx_response("milk-production-summary", headers, rows)