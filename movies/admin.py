from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ('name', )


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 1
    raw_id_fields = ['person']


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'creation_date', 'rating']
    list_filter = ('type', 'creation_date')
    search_fields = ('title', 'description', 'id')
    inlines = (GenreFilmworkInline, PersonFilmworkInline)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', ]
    search_fields = ('full_name', )
