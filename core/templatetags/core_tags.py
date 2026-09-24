"""Custom template tags and filters."""

from datetime import date

from django import template

register = template.Library()


@register.filter
def currency(value):
    """Format a numeric value with two decimals and thousands separators."""
    try:
        return "{:,.2f}".format(float(value or 0))
    except (TypeError, ValueError):
        return "0.00"


@register.filter
def age_from(value):
    """Return a compact age string like '3y 4m' from a birth date."""
    if not value:
        return "-"
    today = date.today()
    years = today.year - value.year
    months = today.month - value.month
    if months < 0:
        years -= 1
        months += 12
    if years < 0:
        return "-"
    out = f"{years}y" if years else ""
    if months or not out:
        out += f" {months}m"
    return out.strip()


@register.filter
def badge(value):
    """Map a status/value to a Tailwind badge colour class set."""
    mapping = {
        "Active": "bg-emerald-100 text-emerald-800",
        "Inactive": "bg-gray-100 text-gray-700",
        "Milker": "bg-indigo-100 text-indigo-800",
        "Heifer": "bg-sky-100 text-sky-800",
        "Dry": "bg-amber-100 text-amber-700",
        "Calf": "bg-rose-100 text-rose-700",
        "Bull": "bg-gray-200 text-gray-800",
        "Weaner": "bg-teal-100 text-teal-800",
        "Yearling": "bg-violet-100 text-violet-800",
        "Sold": "bg-slate-100 text-slate-700",
        "Culled": "bg-rose-100 text-rose-700",
        "Deceased": "bg-rose-100 text-rose-700",
        "Transferred": "bg-sky-100 text-sky-800",
        "Paid": "bg-emerald-100 text-emerald-800",
        "Partial": "bg-amber-100 text-amber-700",
        "Unpaid": "bg-rose-100 text-rose-700",
        "Positive": "bg-emerald-100 text-emerald-800",
        "Negative": "bg-rose-100 text-rose-700",
        "Unconfirmed": "bg-amber-100 text-amber-700",
        "Failed": "bg-rose-100 text-rose-700",
        "Pending": "bg-amber-100 text-amber-700",
        "Conceived": "bg-emerald-100 text-emerald-800",
        "Not Conceived": "bg-rose-100 text-rose-700",
        "Male": "bg-sky-100 text-sky-800",
        "Female": "bg-rose-100 text-rose-700",
        "Born": "bg-emerald-100 text-emerald-800",
        "Purchased": "bg-sky-100 text-sky-800",
        "Morning": "bg-amber-100 text-amber-700",
        "Evening": "bg-indigo-100 text-indigo-800",
        "Income": "bg-emerald-100 text-emerald-800",
        "Expense": "bg-rose-100 text-rose-700",
    }
    return mapping.get(str(value), "bg-gray-100 text-gray-600")