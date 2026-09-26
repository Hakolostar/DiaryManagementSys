"""Printable report views for each domain."""

from datetime import date, timedelta

from django.db.models import Count, Sum
from django.views.generic import TemplateView

from core.views import AppMixin
from core.xlsx import build_xlsx_response

from milk.models import MilkProduction
from herd.models import Animal
from breeding.models import Calving, Heat, Insemination, Pregnancy
from health.models import Treatment, Vaccination, VetVisit


class BaseReportView(AppMixin, TemplateView):
    """Adds a report date range to the template context plus XLSX export."""

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

    def get(self, request, *args, **kwargs):
        """Serve an Excel download when ``?format=xlsx`` is requested."""
        if request.GET.get("format") == "xlsx":
            return self.render_xlsx()
        return super().get(request, *args, **kwargs)

    def render_xlsx(self):
        ctx = self.get_context_data()
        headers, rows = self.xlsx_export(ctx)
        return build_xlsx_response(self.xlsx_filename(), headers, rows)

    def xlsx_filename(self):
        return self.title

    def xlsx_export(self, ctx):
        """Return (headers, rows) for the Excel export.

        Override in subclasses to customise the exported sheet.
        """
        return [], []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["request"] = self.request
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

    def xlsx_export(self, ctx):
        headers = ["Date", "Animal", "Session", "Quantity (L)"]
        rows = [
            [r.date, r.animal.full_name, r.session, r.quantity]
            for r in ctx["records"]
        ]
        return headers, rows


class HerdReportView(BaseReportView):
    template_name = "reports/herd_report.html"
    title = "Herd Report"
    range_days = 0

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["herd"] = Animal.objects.select_related("breed").all()
        ctx["by_status"] = list(
            Animal.objects.values("status")
            .annotate(n=Count("id"))
            .order_by("status")
        )
        ctx["by_category"] = list(
            Animal.objects.values("category")
            .annotate(n=Count("id"))
            .order_by("category")
        )
        ctx["by_breed"] = list(
            Animal.objects.values("breed__name")
            .annotate(n=Count("id"))
            .order_by("-n")[:8]
        )
        return ctx

    def xlsx_export(self, ctx):
        headers = ["Tag", "Name", "Breed", "Sex", "Category", "Status", "D.O.B"]
        rows = [
            [a.tag_number, a.name, str(a.breed) if a.breed else "", a.sex, a.category, a.status, a.dob]
            for a in ctx["herd"]
        ]
        return headers, rows


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

    def xlsx_export(self, ctx):
        headers = ["Animal", "Date", "Description", "Type"]
        rows = []
        for a in ctx["ais"]:
            rows.append([a.animal.full_name, a.service_date, a.result, "Insemination"])
        for c in ctx["calvings"]:
            rows.append([c.animal.full_name, c.calving_date, c.calving_type, "Calving"])
        return headers, rows


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

    def xlsx_export(self, ctx):
        headers = ["Animal", "Description", "Type", "Cost"]
        rows = []
        for v in ctx["vaccinations"]:
            rows.append([v.animal.full_name, v.vaccine_name, "Vaccination", v.cost])
        for t in ctx["treatments"]:
            rows.append([t.animal.full_name, t.diagnosis, "Treatment", t.cost])
        for v in ctx["vet_visits"]:
            rows.append([v.animal.full_name, v.reason, "Vet visit", v.cost])
        return headers, rows


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

    def xlsx_export(self, ctx):
        headers = ["Date", "Feed", "Animal", "Qty", "Cost"]
        rows = [
            [
                c.date,
                c.feed_item.name,
                c.animal.full_name if c.animal else "Herd group",
                c.quantity,
                c.total_cost,
            ]
            for c in ctx["consumptions"]
        ]
        return headers, rows


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

    def xlsx_export(self, ctx):
        headers = ["Date", "Category", "Description", "Amount", "Type"]
        rows = [
            [
                t.transaction_date,
                t.category.name,
                t.description,
                t.amount,
                "Income" if t.is_income else "Expense",
            ]
            for t in ctx["transactions"]
        ]
        return headers, rows


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

    def xlsx_export(self, ctx):
        headers = ["Sale #", "Customer", "Type", "Total", "Status"]
        rows = [
            [s.sale_number, s.customer.name, s.sale_type, s.total, s.payment_status]
            for s in ctx["sales"]
        ]
        return headers, rows


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

    def xlsx_export(self, ctx):
        headers = ["Item", "Category", "Unit", "Stock", "Unit Cost", "Value", "Status"]
        rows = [
            [
                i.name,
                i.category,
                i.unit,
                i.current_stock,
                i.unit_cost,
                i.stock_value,
                "Low stock" if i.is_low else "In stock",
            ]
            for i in ctx["items"]
        ]
        return headers, rows
