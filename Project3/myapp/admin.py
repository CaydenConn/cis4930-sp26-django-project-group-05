from django.contrib import admin
from .models import Genre, Movie, WeatherRecord
# Register your models here.

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'genre', 'rating', 'score', 'director', 'budget', 'gross', 'runtime')
    list_filter = ('rating', 'genre', 'year')
    search_fields = ('name', 'director', 'star', 'company')
    list_per_page = 25

@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ('city', 'date', 'temp_max', 'temp_min', 'uv_index')
    list_filter = ('city',)
    search_fields = ('city',)
    list_per_page = 25