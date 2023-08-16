import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):

    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Person(UUIDMixin, TimeStampedMixin):

    full_name = models.CharField(max_length=255, verbose_name='ФИО')

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'

    def __str__(self) -> str:
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):

    CHOICE_TYPE = (
        ('кино', 'movie'),
        ('тв шоу', 'tv_show')
    )

    title = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    creation_date = models.DateField(blank=True, verbose_name='Дата премьеры')
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                               blank=True, verbose_name='Рейтинг')
    type = models.CharField(max_length=100, choices=CHOICE_TYPE, default='movie', verbose_name='Тип')
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self) -> str:
        return self.title


class GenreFilmwork(UUIDMixin):

    film_work = models.ForeignKey(Filmwork, verbose_name='Фильм', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, verbose_name='Жанр', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class PersonFilmwork(UUIDMixin):

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.TextField(null=True, verbose_name='Роль')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
