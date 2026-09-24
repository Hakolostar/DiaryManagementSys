"""Admin configuration for the finance module."""

from django.contrib import admin

from .models import FinanceCategory, Transaction


@admin.register(FinanceCategory)
class FinanceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category_type")
    list_filter = ("category_type",)
    search_fields = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_date", "category", "amount", "payment_method")
    list_filter = ("payment_method", "transaction_date", "category__category_type")
    search_fields = ("description", "reference_number", "category__name")