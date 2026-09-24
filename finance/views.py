"""Views for the finance module."""

from django.urls import reverse_lazy

from core.views import AppCreateView, AppDeleteView, AppListView, AppUpdateView

from .forms import CategoryForm, TransactionForm
from .models import FinanceCategory, Transaction


class TransactionListView(AppListView):
    model = Transaction
    template_name = "finance/transaction_list.html"
    context_object_name = "transactions"
    title = "Finance"

    def get_queryset(self):
        qs = Transaction.objects.select_related("category").all()
        ttype = self.request.GET.get("type", "")
        if ttype in ("Income", "Expense"):
            qs = qs.filter(category__category_type=ttype)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        income = sum(float(t.amount) for t in qs if t.is_income)
        expense = sum(float(t.amount) for t in qs if not t.is_income)
        ctx["type"] = self.request.GET.get("type", "")
        ctx["income_total"] = income
        ctx["expense_total"] = expense
        ctx["balance"] = income - expense
        return ctx


class TransactionAddView(AppCreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy("finance:transaction_list")
    title = "Add Transaction"
    cancel_url = reverse_lazy("finance:transaction_list")
    success_message = "Transaction added."


class TransactionEditView(AppUpdateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy("finance:transaction_list")
    title = "Edit Transaction"
    cancel_url = reverse_lazy("finance:transaction_list")
    success_message = "Transaction updated."


class TransactionDeleteView(AppDeleteView):
    model = Transaction
    success_url = reverse_lazy("finance:transaction_list")
    success_message = "Transaction deleted."


class CategoryListView(AppListView):
    model = FinanceCategory
    template_name = "finance/category_list.html"
    context_object_name = "categories"
    title = "Finance Categories"


class CategoryAddView(AppCreateView):
    model = FinanceCategory
    form_class = CategoryForm
    success_url = reverse_lazy("finance:category_list")
    title = "Add Category"
    cancel_url = reverse_lazy("finance:category_list")
    success_message = "Category added."


class CategoryEditView(AppUpdateView):
    model = FinanceCategory
    form_class = CategoryForm
    success_url = reverse_lazy("finance:category_list")
    title = "Edit Category"
    cancel_url = reverse_lazy("finance:category_list")
    success_message = "Category updated."


class CategoryDeleteView(AppDeleteView):
    model = FinanceCategory
    success_url = reverse_lazy("finance:category_list")
    success_message = "Category deleted."