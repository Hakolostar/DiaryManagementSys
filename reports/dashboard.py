"""Dashboard view with KPIs, alerts and Chart.js datasets."""

import json
from datetime import date, timedelta

from django.db.models import Sum
from django.views.generic import TemplateView

from core.views import AppMixin

from finance.models import Transaction
from herd.models import Animal
from milk.models import MilkProduction
from health.models import Medicine
from breeding.models import Heat, Pregnancy
from health.models import Vaccination


def monthly_range(offset):
    """Return (start, end) dates for a month offset from the current month."""
    today = date.today()
    first = today.replace(day=1)
    month = first.month - offset
    year = first.year
    while month <= 0:
        month += 12
        year -= 1
    start = date(year, month, 1)
    end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    return start, end


class DashboardView(AppMixin, TemplateView):
    template_name = "reports/dashboard.html"
    title = "Dashboard"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        month_start = today.replace(day=1)

        # --- Key figures ---
        ctx["total_animals"] = Animal.objects.filter(status="Active").count()
        ctx["milkers"] = Animal.objects.filter(
            status="Active", category="Milker"
        ).count()
        ctx["today_milk"] = MilkProduction.objects.filter(date=today).aggregate(
            s=Sum("quantity")
        )["s"] or 0
        ctx["month_milk"] = MilkProduction.objects.filter(
            date__gte=month_start
        ).aggregate(s=Sum("quantity"))["s"] or 0

        incomes = Transaction.objects.filter(
            category__category_type="Income", transaction_date__gte=month_start
        )
        expenses = Transaction.objects.filter(
            category__category_type="Expense", transaction_date__gte=month_start
        )
        ctx["month_income"] = sum(float(t.amount) for t in incomes)
        ctx["month_expense"] = sum(float(t.amount) for t in expenses)
        ctx["month_balance"] = ctx["month_income"] - ctx["month_expense"]

        # --- Milk trend (last 14 days) ---
        days = [today - timedelta(days=i) for i in range(13, -1, -1)]
        daily = {}
        for row in MilkProduction.objects.filter(date__gte=days[0], date__lte=today):
            daily[row.date] = daily.get(row.date, 0) + row.quantity
        ctx["milk_labels"] = [d.strftime("%d %b") for d in days]
        ctx["milk_values"] = [float(daily.get(d, 0)) for d in days]

        am = MilkProduction.objects.filter(
            date__gte=month_start, session="Morning"
        ).aggregate(s=Sum("quantity"))["s"] or 0
        pm = MilkProduction.objects.filter(
            date__gte=month_start, session="Evening"
        ).aggregate(s=Sum("quantity"))["s"] or 0
        ctx["am_total"] = am
        ctx["pm_total"] = pm

        # --- Herd composition ---
        composition = {}
        for animal in Animal.objects.filter(status="Active"):
            composition[animal.category or "Unknown"] = (
                composition.get(animal.category, 0) + 1
            )
        ctx["herd_labels"] = list(composition.keys())
        ctx["herd_values"] = list(composition.values())

        # --- Alerts ---
        ctx["due_heats"] = Heat.objects.filter(
            expected_heat_date__lte=today + timedelta(days=7)
        ).select_related("animal")[:8]
        ctx["due_calvings"] = Pregnancy.objects.filter(
            expected_calving_date__lte=today + timedelta(days=14)
        ).select_related("animal")[:8]
        ctx["due_vaccinations"] = Vaccination.objects.filter(
            next_due_date__lte=today + timedelta(days=30)
        ).select_related("animal")[:8]
        ctx["low_medicines"] = [m for m in Medicine.objects.all() if m.is_low][:8]

        # --- Finance chart (last 6 months) ---
        labels, income_vals, expense_vals = [], [], []
        for offset in range(5, -1, -1):
            start, end = monthly_range(offset)
            inc = sum(
                float(t.amount)
                for t in Transaction.objects.filter(
                    category__category_type="Income",
                    transaction_date__gte=start,
                    transaction_date__lt=end,
                )
            )
            exp = sum(
                float(t.amount)
                for t in Transaction.objects.filter(
                    category__category_type="Expense",
                    transaction_date__gte=start,
                    transaction_date__lt=end,
                )
            )
            labels.append(start.strftime("%b"))
            income_vals.append(inc)
            expense_vals.append(exp)
        ctx["finance_labels"] = labels
        ctx["finance_income"] = income_vals
        ctx["finance_expense"] = expense_vals
        return self._jsonify(ctx)

    def _jsonify(self, ctx):
        for key in (
            "milk_labels",
            "milk_values",
            "herd_labels",
            "herd_values",
            "finance_labels",
            "finance_income",
            "finance_expense",
        ):
            if key in ctx:
                ctx[key + "_json"] = json.dumps(ctx[key])
        return ctx