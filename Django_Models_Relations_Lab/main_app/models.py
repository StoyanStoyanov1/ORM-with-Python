from django.db import models
from django.utils import timezone


# Create your models here


class Lecturer(models.Model):
    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subject(models.Model):
    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=10,
    )

    lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Student(models.Model):
    student_id = models.CharField(
        primary_key=True,
        max_length=10,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    birth_date = models.DateField()

    email = models.EmailField(
        unique=True
    )

    subjects = models.ManyToManyField(
        to=Subject,
        through='StudentEnrollment'

    )


class StudentEnrollment(models.Model):
    GRADE_CHOICES = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("F", "F"),
    )

    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE,
    )

    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE,
    )

    enrollment_date = models.DateField(
        default=timezone.now()
    )

    grade = models.CharField(
        max_length=1,
        choices=GRADE_CHOICES,
    )

class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(
        to=Lecturer,
        on_delete=models.CASCADE,
    )

    email = models.EmailField(
        unique=True,
    )

    bio = models.TextField(
        blank=True,
        null=True,
    )

    office_location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
