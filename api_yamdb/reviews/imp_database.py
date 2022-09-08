import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

#импорт User

NAME_MODEL_FILE = {
    'user': (User, 'users.csv'),
}


class Command(BaseCommand):
    help = 'Load data from csv file to model'

    @staticmethod
    def get_csv_file(filename):
        return os.path.join(settings.BASE_DIR, 'static', 'data', filename)

    @staticmethod
    def clear_model(model):
        model.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def print_to_terminal(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def load_model(self, model_name, field_names):
        model, file_path = MODEL.get(model_name)
        with open(self.get_csv_file(file_path)) as file:
            reader = csv.reader(file, delimiter=',')
            self.clear_model(model)
            line = 0
            for row in reader:
                if row != '' and line > 0:
                    params = dict(zip(field_names, row))
                    _, created = model.objects.get_or_create(**params)
                line += 1
        self.print_to_terminal(f'{line - 1} objects added to {model_name}')

    def load_user(self):
        self.load_model(
            'user',
            ['id', 'username', 'email', 'role', 'bio',
             'first_name', 'last_name']
        )

    def handle(self, *args, **kwargs):
        self.load_user()
