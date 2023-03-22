import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

path = 'static/data/'


class Command(BaseCommand):
    """Заполняет базу данных из csv файлов"""

    help = 'Заполняет базу данных данными из файлов'

    def handle(self, *args, **options):

        # User
        with open(f'{path}users.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                p.save()

        # Category
        with open(f'{path}category.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                p = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                p.save

        # Genre
        with open(f'{path}genre.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                p.save

        # Title
        with open(f'{path}titles.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category']),
                )
                p.save

        # Review
        with open(f'{path}review.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = Review(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                p.save

        # Comment
        with open(f'{path}comments.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = Comment(
                    id=row['id'],
                    review=Review.objects.get(id=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date']
                )
                p.save
