from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=120, unique=True)

	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	sku = models.CharField(max_length=100, blank=True)
	brand = models.CharField(max_length=100, blank=True)
	category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
	
	description = models.TextField(blank=True)
	specs = models.JSONField(blank=True, null=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	stock = models.PositiveIntegerField(default=0)
	available = models.BooleanField(default=True)
	# Prefer storing a single image URL for flexibility in admin
	image_url = models.URLField(blank=True, null=True)
	# Keep FileField for backward compatibility if needed
	main_image = models.ImageField(upload_to='products/', blank=True, null=True)
	is_featured = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return self.name




class ProductImage(models.Model):
	product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
	image = models.ImageField(upload_to='products/gallery/')
	caption = models.CharField(max_length=200, blank=True)

	def __str__(self):
		return f"{self.product.name} image"


class ProductVariant(models.Model):
	product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
	name = models.CharField(max_length=100, help_text='e.g. 64 GB, 128 GB')
	sku = models.CharField(max_length=100, blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField(default=0)
	is_default = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Product Variant'
		verbose_name_plural = 'Product Variants'

	def __str__(self):
		return f"{self.product.name} - {self.name}"

