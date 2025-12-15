from django.core.management.base import BaseCommand
from home.models import Product

class Command(BaseCommand):
    help = 'List product slugs'

    def handle(self, *args, **options):
        slugs = [p.slug for p in Product.objects.all()]
        self.stdout.write(str(slugs))
