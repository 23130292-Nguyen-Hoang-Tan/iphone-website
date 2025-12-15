import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','apple_website.settings')
import django
django.setup()
from home.models import Product
slugs = [p.slug for p in Product.objects.all()]
print(slugs)