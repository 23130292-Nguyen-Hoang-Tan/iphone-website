from django.contrib import admin
from .models import Product, Category, ProductVariant


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'sku', 'price', 'stock', 'available', 'category_id')
	list_filter = ('available', 'created', 'is_featured')
	search_fields = ('name', 'description', 'sku')
	prepopulated_fields = {"slug": ("name",)}
	fieldsets = (
		(None, {'fields': ('name', 'slug', 'sku', 'brand', 'category', 'image_url', 'main_image')}),
		('Pricing', {'fields': ('price', 'old_price')}),
		('Inventory', {'fields': ('stock', 'available')}),
		('Content', {'fields': ('description', 'specs')}),
	)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


# attach inline to Product admin
ProductAdmin.inlines = [ProductVariantInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	prepopulated_fields = {"slug": ("name",)}
