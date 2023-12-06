import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Review, Article


# Import your models here
# Create and run your queries within functions

def get_authors(search_name=None, search_email=None):
    if search_name is not None or search_email is not None:
        query = Q()
        if search_name is not None:
            query &= Q(full_name__icontains=search_name)
        if search_email is not None:
            query &= Q(email__icontains=search_email)

        authors = Author.objects.all().filter(query).order_by('-full_name')

        if authors:
            result = [
                f"Author: {author.full_name}, email: {author.email}, status: {'Banned' if author.is_banned else 'Not Banned'}"
                for author in authors]

            return '\n'.join(result)

    return ""


def get_top_publisher():
    authors = Author.objects.get_authors_by_article_count()

    result = ''

    if authors:
        top_author = authors.first()
        if top_author.num_article:
            result = f"Top Author: {top_author.full_name} with {top_author.num_article} published articles."

    return result


def get_top_reviewer():
    reviewers = Author.objects.all().annotate(num_reviews=Count('review')).filter(num_reviews__gt=0).order_by(
        '-num_reviews', 'email')

    result = ''
    if reviewers:
        top_reviewer = reviewers.first()
        if top_reviewer.num_reviews:
            result = f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_reviews} published reviews."

    return result


def get_latest_article():
    articles = (Article.objects.annotate(num_reviews=Count('review'), avg_rating=Avg('review__rating'))
                .order_by('published_on'))

    if articles.exists():
        last_article = articles.last()

        author_names = ', '.join(author.full_name for author in last_article.authors.all().order_by('full_name'))
        avg_rating = last_article.avg_rating or 0
        article_title = last_article.title
        num_reviews = last_article.num_reviews

        result = (f"The latest article is: {article_title}. Authors: {author_names}. "
                  f"Reviewed: {num_reviews} times. Average Rating: {avg_rating:.2f}.")
    else:
        result = ""

    return result


def get_top_rated_article():
    articles = (Article.objects.annotate(num_reviews=Count('review'), avg_rating=Avg('review__rating'))
                .filter(num_reviews__gt=0)
                .order_by('-avg_rating', 'title'))

    if articles.exists():
        top_rated_article = articles.first()
        num_reviews = top_rated_article.num_reviews
        article_title = top_rated_article.title
        avg_rating = top_rated_article.avg_rating or 0

        result = (f"The top-rated article is: {article_title}, with an average rating of {avg_rating:.2f}, "
                  f"reviewed {num_reviews} times.")
    else:
        result = ""

    return result


def ban_author(email=None):
    if email is not None:
        author = Author.objects.all().filter(email=email)

        if author:
            author = author.first()
            num_reviews = Review.objects.filter(author=author).count()
            Review.objects.filter(author=author).delete()
            author.is_banned = True
            author.save()

            return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."

    return "No authors banned."
