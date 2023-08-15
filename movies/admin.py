from django.contrib import admin
from .models import Genre, Filmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ['created', ]


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'creation_date', 'rating', 'type']
