# my_app/admin.py
from django.contrib import admin
from .models import Category, Product, ProductVariant, Specification, News


# Inline cho phép bạn thêm biến thể ngay trong trang Product


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # Số dòng trống cho biến thể mới
    fields = ('storage', 'color', 'price',
              'discount_percent', 'stock_quantity', 'image')

# 1. Định nghĩa Inline cho Specification


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1  # Số lượng form trống mặc định
    fields = ('order', 'key', 'value')

# Tùy chỉnh hiển thị trong trang Admin (optional nhưng được khuyến khích)


class NewsAdmin(admin.ModelAdmin):
    # Các trường hiển thị trong danh sách tin tức
    list_display = ('title', 'published_date', 'source', 'is_store_info')
    # Các trường có thể tìm kiếm
    search_fields = ('title', 'summary', 'source')
    # Thêm bộ lọc theo ngày
    list_filter = ('published_date', 'is_store_info')


# Đăng ký model với tùy chỉnh
admin.site.register(News, NewsAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Tự động điền slug


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [SpecificationInline, ProductVariantInline]
    list_display = ('name', 'category', 'is_new', 'is_bestseller')
    list_filter = ('category', 'is_new', 'is_bestseller')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'category', 'slug', 'chip_type')
        }),
        ('Mô tả & Thông số', {
            'fields': ('description',),
        }),
        ('Tình trạng & Bảo hành', {
            'fields': ('is_new', 'is_bestseller', 'warranty_months', 'shipping_info')
        }),
    )
