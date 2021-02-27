from django.core.management.base import BaseCommand
from quizyapp.utils.category import init_category_list_from_api_if_none_available
from quizyapp.models import Category

class Command(BaseCommand):
    def handle(self, *args, **options):

        self.stdout.write('running init_category_list_from_api_if_none_available...')
        self.stdout.write(f'Category objects in db BEFORE running: {Category.objects.all().count()}')
        init_category_list_from_api_if_none_available()
        self.stdout.write(f'Category objects in db AFTER running: {Category.objects.all().count()}')
