from django.db import models


class ChoicesCategory(models.TextChoices):
    TECHNOLOGY = ("Technology", 'Technology')
    SCIENCE = ("Science", "Science")
    EDUCATION = ("Education", "Education")
