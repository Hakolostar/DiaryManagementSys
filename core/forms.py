"""Reusable form helpers that give every form a consistent, modern Tailwind look."""

from django import forms


class StyledFormMixin:
    """Mixin that applies Tailwind CSS classes to every field widget."""

    field_class = (
        "w-full rounded-lg border border-gray-300 bg-white py-2 px-3 text-sm "
        "text-gray-800 shadow-sm focus:border-emerald-500 "
        "focus:outline-none focus:ring-2 focus:ring-emerald-200"
    )
    checkbox_class = (
        "h-4 w-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = self.checkbox_class
                continue
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault("rows", 3)
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(
                    attrs={"type": "date", "class": self.field_class}
                )
            elif isinstance(
                field, (forms.DecimalField, forms.FloatField, forms.IntegerField)
            ):
                field.widget = forms.NumberInput(
                    attrs={"class": self.field_class, "step": "0.01"}
                )
            else:
                field.widget.attrs.setdefault("class", self.field_class)


class StyledModelForm(StyledFormMixin, forms.ModelForm):
    """ModelForm with consistent Tailwind styling."""


class StyledForm(StyledFormMixin, forms.Form):
    """Plain Form with consistent Tailwind styling."""