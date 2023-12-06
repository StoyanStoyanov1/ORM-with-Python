from django.core import validators
from django.db import models
from main_app.mixins import Person, ChoicesGenre
from .managers import DirectorManager


class Director(Person):
    years_of_experience = models.SmallIntegerField(
        validators=[validators.MinValueValidator(0)],
        default=0
    )

    objects = DirectorManager()


class Actor(Person):
    is_awarded = models.BooleanField(
        default=False,
    )

    last_updated = models.DateTimeField(
        auto_now_add=True,
    )


class Movie(models.Model):
    title = models.CharField(
        max_length=150,
        validators=[validators.MinLengthValidator(5),
                    validators.MaxLengthValidator(150)]
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True,
    )

    genre = models.CharField(
        max_length=6,
        choices=ChoicesGenre.choices,
        default=ChoicesGenre.OTHER,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(10)],
        default=0,
    )

    is_classic = models.BooleanField(
        default=False,
    )

    is_awarded = models.BooleanField(
        default=False,
    )

    last_updated = models.DateTimeField(
        auto_now_add=True,
    )

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='director_movies'
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='starring_actor_movies'
    )

    actors = models.ManyToManyField(
        to=Actor,
        related_name='actor_movies'
    )

