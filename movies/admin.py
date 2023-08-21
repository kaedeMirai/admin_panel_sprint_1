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
    readonly_fields = ['display_person_name']  # Add this line

    def display_person_name(self, instance):
        return instance.person.full_name  # Display the full_name of the person
    display_person_name.short_description = 'Person'  # Set a custom column header


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'creation_date', 'rating']
    list_filter = ('type', 'creation_date')
    search_fields = ('title', 'description')
    inlines = (GenreFilmworkInline, PersonFilmworkInline)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', ]
    search_fields = ('full_name', )
