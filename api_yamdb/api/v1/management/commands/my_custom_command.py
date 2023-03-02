import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Genre


CSV_FILES = {
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv'
}


class Command(BaseCommand):
    help = 'import data from csv flies to database'

    def handle(self, *args, **options):
        for model, filename in CSV_FILES.items():
            with open(filename, encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    try:
                        model.objects.get_or_create(**row)
                    except Exception as error:
                        print(f'Ошибка при импорте {filename}. Ошибка {error}')
