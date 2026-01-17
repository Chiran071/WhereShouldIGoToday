from django.contrib import admin
from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'primary_mood', 'primary_weather', 'rating']
    list_filter = ['city', 'primary_mood', 'primary_weather']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'city', 'image', 'google_maps_url')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Moods', {
            'fields': ('primary_mood', 'secondary_mood', 'tertiary_mood', 'quaternary_mood')
        }),
        ('Weather', {
            'fields': ('primary_weather', 'secondary_weather')
        }),
        ('Budget & Time', {
            'fields': ('min_budget', 'max_budget', 'min_time_hours', 'max_time_hours')
        }),
        ('Rating', {
            'fields': ('rating',)
        }),
    )
