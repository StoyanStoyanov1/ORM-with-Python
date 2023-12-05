from django.contrib import admin
from .models import Pet
from .models import Artifact
from .models import Location
from .models import Car
from .models import Task
from .models import HotelRoom
from .models import Character


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species')
    search_fields = ('name',)


@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    list_display = ('name', 'origin', 'age', 'description', 'is_magical')
    search_fields = ('name',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'population', 'description', 'is_capital')
    search_fields = ('name', 'region')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'year', 'color', 'price', 'price_with_discount')
    search_fields = ('model', 'year', 'price', 'color')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'is_finished')
    search_fields = ('title',)


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'capacity', 'amenities', 'price_per_night', 'is_reserved')
    search_fields = ('room_number', 'price_per_night', 'is_reserved')


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name', 'level')
    search_fields = ('name', 'class_name')
