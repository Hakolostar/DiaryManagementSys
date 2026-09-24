"""Shared mixins and generic views used across every module."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


class AppMixin(LoginRequiredMixin):
    """Login-protected view that supplies shared template context."""

    title = ""
    subtitle = ""
    cancel_url = ""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = self.title
        ctx["subtitle"] = self.subtitle
        ctx["cancel_url"] = self.cancel_url
        return ctx


class SuccessMessageMixin:
    """Add a one-off Django message on successful form submission."""

    success_message = ""

    def form_valid(self, form):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return super().form_valid(form)


class AppListView(AppMixin, ListView):
    paginate_by = 25


class AppCreateView(AppMixin, SuccessMessageMixin, CreateView):
    template_name = "core/form_page.html"


class AppUpdateView(AppMixin, SuccessMessageMixin, UpdateView):
    template_name = "core/form_page.html"


class AppDeleteView(AppMixin, SuccessMessageMixin, DeleteView):
    template_name = "core/confirm_delete.html"