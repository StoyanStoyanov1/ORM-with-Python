import os
import django
from django.utils.datetime_safe import date

from main_app.models import Task

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


