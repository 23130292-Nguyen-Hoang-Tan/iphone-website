from django.core.management.base import BaseCommand
from home.models import Product

class Command(BaseCommand):
    help = 'Copy main_image.url into image_url for products that lack image_url (optionally filter by category slug)'

    def add_arguments(self, parser):
        parser.add_argument('--category', '-c', help='Category slug to filter (e.g. ipad). If omitted, process all products.')

    def handle(self, *args, **options):
        cat = options.get('category')
        qs = Product.objects.all()
        if cat:
            qs = qs.filter(category__slug=cat)
        count = 0
        for p in qs:
            if not p.image_url:
                if p.main_image:
                    try:
                        p.image_url = p.main_image.url
                        p.save(update_fields=['image_url'])
                        count += 1
                        self.stdout.write(f"Updated product {p.pk} -> image_url set to main_image.url")
                    except Exception as e:
                        self.stderr.write(f"Failed to update product {p.pk}: {e}")
        self.stdout.write(self.style.SUCCESS(f"Done. {count} products updated."))
