from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ['created', ]


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 1
    raw_id_fields = ['person']


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'creation_date', 'rating']
    inlines = (GenreFilmworkInline, PersonFilmworkInline)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', ]
