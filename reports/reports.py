"""Printable report views for each domain."""

from datetime import date, timedelta

from django.db.models import Count, Sum
from django.views.generic import TemplateView

from core.views import AppMixin

from milk.models import MilkProduction
from herd.models import Animal
from breeding.models import Calving, Heat, Insemination, Pregnancy
from health.models import Treatment, Vaccination, VetVisit


class BaseReportView(AppMixin, TemplateView):
    """Adds a report date range to the template context."""

    range_days = 30

    def get_range(self):
        today = date.today()
        start = self.request.GET.get("from") or (
            today - timedelta(days=self.range_days)
        )
        end = self.request.GET.get("to") or today
        try:
            start = date.fromisoformat(str(start))
            end = date.fromisoformat(str(end))
        except ValueError:
            start = today - timedelta(days=self.range_days)
            end = today
        return start, end

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        start, end = self.get_range()
        ctx["start_date"] = start
        ctx["end_date"] = end
        return ctx


class MilkReportView(BaseReportView):
    template_name = "reports/milk_report.html"
    title = "Milk Production Report"
    range_days = 14

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        start, end = ctx["start_date"], ctx["end_date"]
        records = MilkProduction.objects.filter(
            date__gte=start, date__lte=end
        ).select_related("animal")
        ctx["records"] = records
        ctx["days"] = list(
            records.order_by("date").values_list("date", flat=True).distinct()
        )
        ctx["total_milk"] = records.aggregate(s=Sum("quantity"))["s"] or 0
        ctx["am_total"] = records.filter(session="Morning").aggregate(
            s=Sum("quantity")
        )["s"] or 0
        ctx["pm_total"] = records.filter(session="Evening").aggregate(
            s=Sum("quantity")
        )["s"] or 0
        avg = (
            records.aggregate(a=Sum("quantity"))["a"] or 0
        ) / max(len(ctx["days"]), 1)
        ctx["avg_daily"] = round(avg, 2)
        return ctx


class HerdReportView(BaseReportView):
    template_name = "reports/herd_report.html"
    title = "Herd Report"
    range_days = 0

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["herd"] = Animal.objects.select_related("breed").all()
        ctx["by_status"] = list(
            Animal.objects.values("status").annotate(n=Count("id")).order_by("status")
        )
        ctx["by_category"] = list(
            Animal.objects.values("category")
            .annotate(n=Count("id"))
            .order_by("category")
        )
        ctx["by_breed"] = list(
            Animal.objects.values("breed__name").annotate(n=Count("id")).order_by(
                "-n"
            )[:8]
        )
        return ctx


class BreedingReportView(BaseReportView):
    template_name = "reports/breeding_report.html"
    title = "Breeding Report"
    range_days = 90

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        start, end = ctx["start_date"], ctx["end_date"]
        ctx["heats"] = Heat.objects.filter(
            heat_date__gte=start, heat_date__lte=end
        ).select_related("animal")
        ctx["ais"] = Insemination.objects.filter(
            service_date__gte=start, service_date__lte=end
        ).select_related("animal")
        ctx["pregnancies"] = Pregnancy.objects.filter(
            check_date__gte=start, check_date__lte=end
        ).select_related("animal")
        ctx["calvings"] = Calving.objects.filter(
            calving_date__gte=start, calving_date__lte=end
        ).select_related("animal")
        done = [i for i in ctx["ais"] if i.result != "Pending"]
        ctx["conception_rate"] = round(
            len([i for i in done if i.result == "Conceived"]) / max(len(done), 1) * 100
        )
        return ctx


class HealthReportView(BaseReportView):
    template_name = "reports/health_report.html"
    title = "Health Report"
    range_days = 90

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        start, end = ctx["start_date"], ctx["end_date"]
        ctx["vaccinations"] = Vaccination.objects.filter(
            date__gte=start, date__lte=end
        ).select_related("animal")
        ctx["treatments"] = Treatment.objects.filter(
            date__gte=start, date__lte=end
        ).select_related("animal")
        ctx["vet_visits"] = VetVisit.objects.filter(
            visit_date__gte=start, visit_date__lte=end
        ).select_related("animal")
        ctx["vaccine_cost"] = sum(float(v.cost) for v in ctx["vaccinations"])
        ctx["treatment_cost"] = sum(float(t.cost) for t in ctx["treatments"])
        ctx["vet_cost"] = sum(float(v.cost) for v in ctx["vet_visits"])
        return ctx


class FeedReportView(BaseReportView):
    template_name = "reports/feed_report.html"
    title = "Feed Report"
    range_days = 30

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        start, end = ctx["start_date"], ctx["end_date"]
        from feed.models import FeedConsumption, FeedPurchase

        ctx["consumptions"] = FeedConsumption.objects.filter(
            date__gte=start, date__lte=end
        ).select_related("feed_item", "animal")
        ctx["purchases"] = FeedPurchase.objects.filter(
            purchase_date__gte=start, purchase_date__lte=end
        ).select_related("feed_item")
        ctx["consumption_cost"] = sum(
            float(c.total_cost) for c in ctx["consumptions"]
        )
        ctx["purchase_cost"] = sum(float(p.total_cost) for p in ctx["purchases"])
        return ctx


class FinanceReportView(BaseReportView):
    template_name = "reports/finance_report.html"
    title = "Finance Report"
    range_days = 30

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        start, end = ctx["start_date"], ctx["end_date"]
        from finance.models import Transaction
        from employees.models import Advance, SalaryPayment

        ctx["transactions"] = Transaction.objects.filter(
            transaction_date__gte=start, transaction_date__lte=end
        ).select_related("category")
        ctx["income_total"] = sum(
            float(t.amount) for t in ctx["transactions"] if t.is_income
        )
        ctx["expense_total"] = sum(
            float(t.amount) for t in ctx["transactions"] if not t.is_income
        )
        ctx["salaries"] = SalaryPayment.objects.filter(
            paid_date__gte=start, paid_date__lte=end
        ).select_related("employee")
        ctx["salary_total"] = sum(float(p.net) for p in ctx["salaries"])
        ctx["advanced"] = sum(
            float(a.amount)
            for a in Advance.objects.filter(
                advance_date__gte=start, advance_date__lte=end, repaid=False
            )
        )
        by_cat = {}
        for t in ctx["transactions"]:
            by_cat[t.category.name] = by_cat.get(t.category.name, 0) + float(t.amount)
        ctx["by_category"] = sorted(by_cat.items(), key=lambda x: x[1], reverse=True)
        return ctx


class SalesReportView(BaseReportView):
    template_name = "reports/sales_report.html"
    title = "Sales & Purchases Report"
    range_days = 30

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        start, end = ctx["start_date"], ctx["end_date"]
        from sales.models import Sale
        from purchases.models import Purchase

        ctx["sales"] = Sale.objects.filter(
            sale_date__gte=start, sale_date__lte=end
        ).select_related("customer")
        ctx["purchases"] = Purchase.objects.filter(
            purchase_date__gte=start, purchase_date__lte=end
        ).select_related("supplier")
        ctx["sales_total"] = sum(float(s.total) for s in ctx["sales"])
        ctx["purchase_total"] = sum(float(p.total) for p in ctx["purchases"])
        ctx["sales_outstanding"] = sum(
            float(s.balance) for s in ctx["sales"] if s.balance > 0
        )
        ctx["purchase_outstanding"] = sum(
            float(p.balance) for p in ctx["purchases"] if p.balance > 0
        )
        return ctx


class InventoryReportView(BaseReportView):
    template_name = "reports/inventory_report.html"
    title = "Inventory Report"
    range_days = 0

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from inventory.models import InventoryItem

        items = InventoryItem.objects.all()
        ctx["items"] = items
        ctx["total_value"] = sum(float(i.stock_value) for i in items)
        ctx["low_items"] = [i for i in items if i.is_low]
        return ctx