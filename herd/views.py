"""Views for the herd module — Animal Master, Breeds, Movements and History."""

from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView

from core.views import AppCreateView, AppDeleteView, AppListView, AppMixin, AppUpdateView

from .forms import AnimalForm, AnimalMovementForm, BreedForm
from .models import Animal, AnimalMovement, Breed


def build_timeline(animal, limit=60):
    """Compose a chronological activity timeline for one animal."""
    from breeding.models import Calving, Heat, Insemination, Pregnancy
    from health.models import Treatment, Vaccination, VetVisit
    from milk.models import MilkProduction, MilkQuality

    events = []
    for mv in animal.movements.all():
        events.append((mv.movement_date, "Movement", str(mv.movement_type)))
    for rec in MilkProduction.objects.filter(animal=animal):
        events.append((rec.date, "Milk", f"{rec.session}: {rec.quantity} L"))
    for rec in MilkQuality.objects.filter(animal=animal):
        events.append((rec.date, "Milk Quality", f"Fat {rec.fat_pct}%"))
    for rec in Heat.objects.filter(animal=animal):
        events.append((rec.heat_date, "Heat", "Heat detected"))
    for rec in Insemination.objects.filter(animal=animal):
        events.append(
            (rec.service_date, "AI", f"Insemination ({rec.bull_name or 'NA'})")
        )
    for rec in Pregnancy.objects.filter(animal=animal):
        events.append((rec.check_date, "Pregnancy", rec.diagnosis))
    for rec in Calving.objects.filter(animal=animal):
        events.append((rec.calving_date, "Calving", rec.calving_type))
    for rec in Vaccination.objects.filter(animal=animal):
        events.append((rec.date, "Vaccination", rec.vaccine_name))
    for rec in Treatment.objects.filter(animal=animal):
        events.append((rec.date, "Treatment", rec.diagnosis))
    for rec in VetVisit.objects.filter(animal=animal):
        events.append((rec.visit_date, "Vet Visit", rec.reason))
    events = [e for e in events if e[0]]
    events.sort(key=lambda x: x[0], reverse=True)
    return events[:limit]


class AnimalListView(AppListView):
    model = Animal
    template_name = "herd/animal_list.html"
    context_object_name = "animals"
    title = "Animal Master"

    def get_queryset(self):
        qs = Animal.objects.select_related("breed").all()
        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()
        if q:
            qs = qs.filter(
                Q(tag_number__icontains=q)
                | Q(name__icontains=q)
                | Q(breed__name__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["current_status"] = self.request.GET.get("status", "")
        ctx["active_count"] = Animal.objects.filter(status="Active").count()
        return ctx


class AnimalTableView(AnimalListView):
    """HTMX partial that renders just the animal table."""

    template_name = "herd/_animal_table.html"


class AnimalAddView(AppCreateView):
    model = Animal
    form_class = AnimalForm
    success_url = reverse_lazy("herd:animal_list")
    title = "Register Animal"
    cancel_url = reverse_lazy("herd:animal_list")
    success_message = "Animal registered successfully."


class AnimalEditView(AppUpdateView):
    model = Animal
    form_class = AnimalForm
    success_url = reverse_lazy("herd:animal_list")
    title = "Edit Animal"
    cancel_url = reverse_lazy("herd:animal_list")
    success_message = "Animal details updated."


class AnimalDeleteView(AppDeleteView):
    model = Animal
    success_url = reverse_lazy("herd:animal_list")
    success_message = "Animal record deleted."


class AnimalDetailView(AppMixin, DetailView):
    model = Animal
    template_name = "herd/animal_detail.html"
    context_object_name = "animal"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = f"Animal — {self.object.tag_number}"
        ctx["timeline"] = build_timeline(self.object)
        return ctx


class BreedListView(AppListView):
    model = Breed
    template_name = "herd/breed_list.html"
    context_object_name = "breeds"
    title = "Breeds"

    def get_queryset(self):
        return Breed.objects.annotate(animal_count=Count("animals")).order_by("name")


class BreedAddView(AppCreateView):
    model = Breed
    form_class = BreedForm
    success_url = reverse_lazy("herd:breed_list")
    title = "Add Breed"
    cancel_url = reverse_lazy("herd:breed_list")
    success_message = "Breed added."


class BreedEditView(AppUpdateView):
    model = Breed
    form_class = BreedForm
    success_url = reverse_lazy("herd:breed_list")
    title = "Edit Breed"
    cancel_url = reverse_lazy("herd:breed_list")
    success_message = "Breed updated."


class BreedDeleteView(AppDeleteView):
    model = Breed
    success_url = reverse_lazy("herd:breed_list")
    success_message = "Breed deleted."


class MovementListView(AppListView):
    model = AnimalMovement
    template_name = "herd/movement_list.html"
    context_object_name = "movements"
    title = "Animal Movement"

    def get_queryset(self):
        qs = AnimalMovement.objects.select_related("animal").all()
        animal = self.request.GET.get("animal", "").strip()
        if animal:
            qs = qs.filter(animal__tag_number__icontains=animal)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["animal_q"] = self.request.GET.get("animal", "")
        return ctx


class MovementAddView(AppCreateView):
    model = AnimalMovement
    form_class = AnimalMovementForm
    success_url = reverse_lazy("herd:movement_list")
    title = "Record Movement"
    cancel_url = reverse_lazy("herd:movement_list")
    success_message = "Movement recorded."

    def get_initial(self):
        initial = super().get_initial()
        animal_id = self.request.GET.get("animal")
        if animal_id:
            initial["animal"] = animal_id
        return initial


class MovementDeleteView(AppDeleteView):
    model = AnimalMovement
    success_url = reverse_lazy("herd:movement_list")
    success_message = "Movement deleted."


class HerdHistoryView(AppMixin, TemplateView):
    template_name = "herd/history.html"
    title = "Animal History"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        animal_id = self.request.GET.get("animal", "")
        ctx["animals"] = Animal.objects.all()
        ctx["animal_id"] = animal_id
        ctx["events"] = build_herd_timeline(animal_id)
        return ctx


def build_herd_timeline(animal_id=None, limit=250):
    """Compose a herd-wide activity log, optionally filtered by animal id."""
    from breeding.models import Calving, Heat, Insemination, Pregnancy
    from health.models import Treatment, Vaccination, VetVisit
    from milk.models import MilkProduction

    def filtered(qs):
        if animal_id:
            return qs.filter(animal_id=animal_id)
        return qs

    events = []
    for rec in filtered(AnimalMovement.objects.select_related("animal")).order_by(
        "-movement_date"
    )[:200]:
        events.append((rec.movement_date, "Movement", str(rec), str(rec.animal)))
    for rec in filtered(
        MilkProduction.objects.select_related("animal")
    ).order_by("-date")[:200]:
        events.append(
            (rec.date, "Milk", f"{rec.session}: {rec.quantity} L", str(rec.animal))
        )
    for rec in filtered(Heat.objects.select_related("animal")).order_by("-heat_date")[
        :200
    ]:
        events.append((rec.heat_date, "Heat", "Heat detected", str(rec.animal)))
    for rec in filtered(Insemination.objects.select_related("animal")).order_by(
        "-service_date"
    )[:200]:
        events.append(
            (
                rec.service_date,
                "AI",
                f"Insemination ({rec.bull_name or 'NA'})",
                str(rec.animal),
            )
        )
    for rec in filtered(Pregnancy.objects.select_related("animal")).order_by(
        "-check_date"
    )[:200]:
        events.append((rec.check_date, "Pregnancy", rec.diagnosis, str(rec.animal)))
    for rec in filtered(Calving.objects.select_related("animal")).order_by(
        "-calving_date"
    )[:200]:
        events.append(
            (rec.calving_date, "Calving", rec.calving_type, str(rec.animal))
        )
    for rec in filtered(Vaccination.objects.select_related("animal")).order_by(
        "-date"
    )[:200]:
        events.append((rec.date, "Vaccination", rec.vaccine_name, str(rec.animal)))
    for rec in filtered(Treatment.objects.select_related("animal")).order_by("-date")[
        :200
    ]:
        events.append((rec.date, "Treatment", rec.diagnosis, str(rec.animal)))
    for rec in filtered(VetVisit.objects.select_related("animal")).order_by(
        "-visit_date"
    )[:200]:
        events.append((rec.visit_date, "Vet Visit", rec.reason, str(rec.animal)))
    events = [e for e in events if e[0]]
    events.sort(key=lambda x: x[0], reverse=True)
    return events[:limit]