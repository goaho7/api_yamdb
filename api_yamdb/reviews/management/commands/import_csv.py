import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Review, Title, User, Comment

path = 'static/data/'


class Command(BaseCommand):
    """Заполняет базу данных из csv файлов"""

    help = 'Заполняет базу данных данными из файлов'

    def handle(self, *args, **options):

        # User
        with open(f'{path}users.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user = User(**row)
                user.save()

        # Category
        with open(f'{path}category.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = Category(**row)
                category.save()

        # Genre
        with open(f'{path}genre.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                genre = Genre(**row)
                genre.save()

        # Title
        with open(f'{path}titles.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category']),
                )
                title.save()

        # Review
        with open(f'{path}review.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                review = Review(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                review.save()

        # Comment
        with open(f'{path}comments.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                comment = Comment(
                    id=row['id'],
                    review=Review.objects.get(id=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date']
                )
                comment.save()
