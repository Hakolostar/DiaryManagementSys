"""Account registration and farm profile views."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import FarmProfileForm, RegistrationForm
from .models import FarmProfile


def register(request):
    if request.user.is_authenticated:
        return redirect("reports:dashboard")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get("first_name", "")
            user.last_name = form.cleaned_data.get("last_name", "")
            user.email = form.cleaned_data.get("email", "")
            user.save()
            FarmProfile.objects.create(
                user=user,
                farm_name=form.cleaned_data.get("farm_name", ""),
                phone=form.cleaned_data.get("phone", ""),
            )
            login(request, user)
            messages.success(request, "Welcome! Your farm workspace is ready.")
            return redirect("reports:dashboard")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    profile, _ = FarmProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = FarmProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Farm profile updated.")
            return redirect("accounts:profile")
    else:
        form = FarmProfileForm(instance=profile)
    return render(request, "accounts/profile.html", {"form": form})