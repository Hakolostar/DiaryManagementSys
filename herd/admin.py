"""Admin configuration for the herd module."""

from django.contrib import admin

from .models import Animal, AnimalMovement, Breed


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("name", "purpose", "origin", "avg_milk_yield")
    search_fields = ("name", "purpose")


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("tag_number", "name", "breed", "sex", "category", "status", "dob")
    list_filter = ("status", "category", "sex", "breed")
    search_fields = ("tag_number", "name")
    autocomplete_fields = ("sire", "dam")


@admin.register(AnimalMovement)
class AnimalMovementAdmin(admin.ModelAdmin):
    list_display = (
        "animal",
        "movement_date",
        "movement_type",
        "from_location",
        "to_location",
    )
    list_filter = ("movement_type",)
    search_fields = ("animal__tag_number", "animal__name")