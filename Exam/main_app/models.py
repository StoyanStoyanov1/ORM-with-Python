from django.core import validators
from django.db import models
from main_app.mixins import ChoicesCategory
from main_app.managers import AuthorManager

# Create your models here.

class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[validators.MinLengthValidator(3), ],
    )

    email = models.EmailField(
        unique=True,
    )

    is_banned = models.BooleanField(
        default=False,
    )

    birth_year = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(1900), validators.MaxValueValidator(2005)],
    )

    website = models.URLField(
        null=True,
        blank=True,
    )

    objects = AuthorManager()


class Article(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[validators.MinLengthValidator(5)],
    )

    content = models.TextField(
        validators=[validators.MinLengthValidator(10)],
    )

    category = models.CharField(
        choices=ChoicesCategory.choices,
        max_length=10,
        default="Technology"
    )

    authors = models.ManyToManyField(
        to=Author,
        related_name='article',
    )

    published_on = models.DateTimeField(
        auto_now_add=True,
    )


class Review(models.Model):
    content = models.TextField(
        validators=[validators.MinLengthValidator(10)],
    )

    rating = models.FloatField(
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)],
    )

    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='review',
    )

    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        related_name='review',
    )

    published_on = models.DateTimeField(
        auto_now_add=True,
    )
