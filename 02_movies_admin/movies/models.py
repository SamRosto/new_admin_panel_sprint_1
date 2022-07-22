import uuid

from random import choices
from django.db import models
from django.forms import DateInput
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(TimeStampMixin, UUIDMixin):
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Filmwork(TimeStampMixin, UUIDMixin):
    class TypeChoice(models.TextChoices):
        TV_SHOW = _('tv_show')
        MOVIE = _('movie')


    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    creation_date = models.DateField(_('Premiere Date'), editable=True)
    rating = models.FloatField(_('Rating'), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(_('Type'), max_length=50, choices=TypeChoice.choices, default=TypeChoice.MOVIE)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')


    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = "Кинопроизведение"
        verbose_name_plural = "Кинопроизведения"


class GenreFilmwork(UUIDMixin, models.Model):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class Gender(models.TextChoices):
    male = _('male')
    female = _('female')

class Person(UUIDMixin, models.Model):
    full_name = models.CharField(_('Name'), max_length = 125)
    gender = models.TextField(_('Gender'), choices=Gender.choices, default=None)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Actor')
        verbose_name_plural = _('Actors')


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.TextField(_('Role'), null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"