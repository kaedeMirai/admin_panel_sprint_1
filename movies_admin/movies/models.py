import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    """
    Абстрактный класс, который добавляет повторяющиеся поля
    "создания" и "изменения" в модели.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """
    Абстрактный класс, который добавляет повторяющееся поле uuid
    в качестве первичного ключа к модели.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """
    Модель django, представляющая жанр кинопроизведения.
    """
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self) -> str:
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    """
    Модель, содержащая персонажа, участника кинопроизведения в определённой роли.
    """
    full_name = models.CharField(max_length=255, verbose_name=_('full name'))

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        indexes = [
            models.Index(fields=['full_name'])
        ]

    def __str__(self) -> str:
        return self.full_name


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('film')
    TV_SHOW = 'tv_show', _('tv show')


class Filmwork(UUIDMixin, TimeStampedMixin):
    """
    Модель, содержащая кинопроизведение.
    """
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

    file_path = models.FileField(_('file path'), blank=True, null=True, upload_to='movies/')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film')
        verbose_name_plural = _('films')
        indexes = [
            models.Index(fields=['creation_date'])
        ]

    def __str__(self) -> str:
        return self.title


class GenreFilmwork(UUIDMixin):
    """
    Промежуточная модель, результат связи manytomany, связующая фильм и жанр.
    """
    film_work = models.ForeignKey(Filmwork, verbose_name=_('film'), on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, verbose_name=_('genre'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre')
        verbose_name_plural = _('genre')
        constraints = [
            UniqueConstraint(fields=['film_work', 'genre'], name='film_work_genre_idx')
        ]


class PersonRole(models.TextChoices):
    DIRECTOR = 'director', _('director')
    SCREENWRITER = 'screenwriter', _('screenwriter')
    ACTOR = 'actor', _('actor')


class PersonFilmwork(UUIDMixin):
    """
    Промежуточная модель, результат связи manytomany, связующая фильм и персонажа.
    """
    film_work = models.ForeignKey(Filmwork, verbose_name=_('film'), on_delete=models.CASCADE)
    person = models.ForeignKey(Person, verbose_name=_('person'), on_delete=models.CASCADE)
    role = models.CharField(
        null=True,
        choices=PersonRole.choices,
        default=PersonRole.ACTOR,
        verbose_name=_('role')
        )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('person')
        verbose_name_plural = _('person')
        indexes = [
            models.Index(fields=['film_work']),
            models.Index(fields=['person']),
        ]
        constraints = [
            UniqueConstraint(fields=['film_work', 'person', 'role'], name='film_work_person_idx')
        ]

    def __str__(self) -> str:
        return self.person.full_name
