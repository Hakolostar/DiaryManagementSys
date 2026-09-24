"""Forms for the herd module."""

from core.forms import StyledModelForm

from .models import Animal, AnimalMovement, Breed


class AnimalForm(StyledModelForm):
    class Meta:
        model = Animal
        fields = (
            "tag_number",
            "name",
            "breed",
            "sex",
            "dob",
            "category",
            "status",
            "source",
            "sire",
            "dam",
            "birth_weight",
            "purchase_date",
            "purchase_price",
            "color",
            "notes",
        )


class BreedForm(StyledModelForm):
    class Meta:
        model = Breed
        fields = ("name", "purpose", "origin", "avg_milk_yield", "description")


class AnimalMovementForm(StyledModelForm):
    class Meta:
        model = AnimalMovement
        fields = (
            "animal",
            "movement_date",
            "movement_type",
            "from_location",
            "to_location",
            "reason",
            "notes",
        )