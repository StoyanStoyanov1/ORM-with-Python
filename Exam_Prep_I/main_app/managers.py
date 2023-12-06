from django.db import models


class DirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        return self.annotate(num_movies=models.Count('director_movies')).order_by('-num_movies', 'full_name')
