"""Forms for account registration and farm profile management."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from core.forms import StyledModelForm

from .models import FarmProfile


class RegistrationForm(UserCreationForm):
    farm_name = forms.CharField(max_length=120, label="Dairy / farm name")
    phone = forms.CharField(max_length=30, required=False, label="Phone")
    first_name = forms.CharField(max_length=100, required=False, label="First name")
    last_name = forms.CharField(max_length=100, required=False, label="Last name")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "farm_name", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "w-full rounded-lg border border-gray-300 bg-white py-2 px-3 text-sm "
                "text-gray-800 shadow-sm focus:border-emerald-500 focus:outline-none "
                "focus:ring-2 focus:ring-emerald-200"
            )


class FarmProfileForm(StyledModelForm):
    class Meta:
        model = FarmProfile
        fields = (
            "farm_name",
            "owner_name",
            "phone",
            "email",
            "address",
            "currency",
            "tagline",
        )