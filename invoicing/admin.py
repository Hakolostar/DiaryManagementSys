"""Admin configuration for the invoicing module."""

from django.contrib import admin

from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "invoice_date",
        "customer",
        "delivery_note",
        "driver_name",
        "tax_percent",
        "status",
    )
    list_filter = ("status", "invoice_date")
    search_fields = ("invoice_number", "customer__name", "delivery_note__delivery_order_number")
    inlines = (InvoiceItemInline,)