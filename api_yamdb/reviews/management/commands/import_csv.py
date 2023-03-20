from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genre, Review, Title
import csv

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет базу данных данными из файлов'

    def handle(self, *args, **options):
        with open('static/data/users.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = User(**row)
                title.save()
