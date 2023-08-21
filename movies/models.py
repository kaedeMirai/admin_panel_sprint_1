import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    modified = models.DateTimeField(auto_now=True, verbose_name='изменён')

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):

    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self) -> str:
        return self.name


class Person(UUIDMixin, TimeStampedMixin):

    full_name = models.CharField(max_length=255, verbose_name=_('full name'))

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self) -> str:
        return self.full_name


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('film')
    TV_SHOW = 'tv_show', _('tv_show')


class Filmwork(UUIDMixin, TimeStampedMixin):

    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    creation_date = models.DateField(blank=True, verbose_name=_('creation date'))
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                               blank=True, verbose_name=_('rating'))
    type = models.CharField(
        max_length=10,
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
        verbose_name=_('type')
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film')
        verbose_name_plural = _('films')

    def __str__(self) -> str:
        return self.title


class GenreFilmwork(UUIDMixin):

    film_work = models.ForeignKey(Filmwork, verbose_name=_('film'), on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, verbose_name=_('genre'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genre')


class PersonFilmwork(UUIDMixin):

    film_work = models.ForeignKey(Filmwork, verbose_name=_('film'), on_delete=models.CASCADE)
    person = models.ForeignKey(Person, verbose_name=_('person'), on_delete=models.CASCADE)
    role = models.TextField(null=True, verbose_name=_('role'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Person')
        verbose_name_plural = _('Person')

    def __str__(self) -> str:
        return self.person.full_name
