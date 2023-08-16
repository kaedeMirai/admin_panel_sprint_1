from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ['created', ]


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'creation_date', 'rating', 'type']
    inlines = (GenreFilmworkInline,)
