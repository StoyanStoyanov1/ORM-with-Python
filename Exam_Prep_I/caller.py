import os
import django
from django.db import models
from django.db.models import Q, F, Count
from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query |= query_name & query_nationality
    elif search_name is not None:
        query |= query_name
    else:
        query |= query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""

    result = []

    [result.append(f"Director: {director.full_name}, nationality: {director.nationality}, "
                   f"experience: {director.years_of_experience}") for director in directors]

    return '\n'.join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.num_movies}."


def get_top_actor():
    top_actor = Actor.objects.annotate(num_movie_actor=models.Count('starring_actor_movies'),
                                       avg_movie_rating=models.Avg('starring_actor_movies__rating')).order_by(
        '-num_movie_actor', 'full_name').first()

    if top_actor and top_actor.num_movie_actor:
        title_movies = ', '.join([movie.title for movie in top_actor.starring_actor_movies.all()])
        avg_rating = top_actor.avg_movie_rating

        return f"Top Actor: {top_actor.full_name}, starring in movies: {title_movies}, movies average rating: {avg_rating:.1f}"

    return ""


def get_actors_by_movies_count():
    top_three_actors = Actor.objects.annotate(num_of_movies=Count('actor_movies')).order_by('-num_of_movies', 'full_name')[:3]

    if not top_three_actors or not top_three_actors[0].num_of_movies:
        return ''

    result = [f"{actor.full_name}, participated in {actor.num_of_movies} movies" for actor in top_three_actors]

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    top_movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if top_movie is None:
        return ''

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else "N/A"

    actors = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)

    cast = ', '.join(actors)

    return (f"Top rated awarded movie: {top_movie.title}, "
            f"rating: {top_movie.rating}. "
            f"Starring actor: {starring_actor}. "
            f"Cast: {cast}.")


def increase_rating():
    movies = Movie.objects.filter(is_classic=True, rating__lt=10)

    if not movies:
        return "No ratings increased."

    update_movies = movies.update(rating=F('rating') + 0.1)

    return f"Rating increased for {update_movies} movies."
