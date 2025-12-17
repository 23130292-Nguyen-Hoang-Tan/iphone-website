from django.db import models
from django.utils import timezone
# my_app/models.py

from django.db import models
from django.utils.text import slugify

# --- 1. MODEL PHÂN LOẠI (Category) ---
# Dùng để nhóm các loại sản phẩm (ví dụ: iPhone, iPad, MacBook, Phụ kiện)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Danh mục"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# --- 2. MODEL SẢN PHẨM CHÍNH (Product) ---
# Lưu trữ thông tin chung của một dòng sản phẩm (ví dụ: iPhone 15 Pro Max)


class Product(models.Model):
    # Thông tin cơ bản
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products', verbose_name="Danh mục")
    name = models.CharField(max_length=255, verbose_name="Tên sản phẩm")
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    # THÊM TRƯỜNG MỚI CHO MACBOOK: Chip xử lý
    chip_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Chip xử lý (ví dụ: M1, M2 Pro)"
    )

    # Mô tả và chi tiết
    description = models.TextField(blank=True, verbose_name="Mô tả")

    # Tình trạng và Khuyến mãi
    is_new = models.BooleanField(default=False, verbose_name="Sản phẩm mới")
    is_bestseller = models.BooleanField(
        default=False, verbose_name="Bán chạy nhất")

    # Thông tin giao hàng/bảo hành
    warranty_months = models.IntegerField(
        default=12, verbose_name="Bảo hành (tháng)")
    shipping_info = models.CharField(
        max_length=255, default="Miễn phí toàn quốc", verbose_name="Thông tin vận chuyển")

    class Meta:
        verbose_name_plural = "Sản phẩm"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# --- 3. MODEL BIẾN THỂ SẢN PHẨM (ProductVariant) ---
# Lưu trữ thông tin riêng biệt cho từng biến thể (Dung lượng + Màu sắc + Giá + Tồn kho)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='variants', verbose_name="Sản phẩm gốc")

    # Các thuộc tính tạo nên biến thể (Dựa trên HTML của bạn)
    storage = models.CharField(
        max_length=50, verbose_name="Dung lượng (GB/TB)")
    color = models.CharField(max_length=50, verbose_name="Màu sắc")

    # Thông tin kho và giá
    price = models.DecimalField(
        max_digits=10, decimal_places=0, verbose_name="Giá bán (VNĐ)")
    stock_quantity = models.IntegerField(
        default=0, verbose_name="Số lượng tồn kho")
    discount_percent = models.IntegerField(
        default=0, verbose_name="Phần trăm giảm giá (%)")

    # Hình ảnh riêng biệt cho biến thể
    image = models.ImageField(
        upload_to='iphone_images/', blank=True, null=True, verbose_name="Ảnh biến thể")

    class Meta:
        # Đảm bảo không có 2 biến thể trùng lặp (cùng sản phẩm, cùng dung lượng, cùng màu)
        unique_together = ('product', 'storage', 'color')
        verbose_name_plural = "Biến thể sản phẩm"
        ordering = ['price']

    def final_price(self):
        """Tính toán giá cuối cùng sau khi giảm giá"""
        discount_amount = (self.price * self.discount_percent) / 100
        return self.price - discount_amount

    def __str__(self):
        return f"{self.product.name} - {self.storage} - {self.color}"

# --- MODEL MỚI: Specification (Thông số kỹ thuật) ---


class Specification(models.Model):
    # Khóa ngoại: Liên kết đến Model Product.
    # Một Product có thể có nhiều Specifications.
    product = models.ForeignKey(
        'Product',
        # Đặt tên để truy vấn ngược: product.specifications.all()
        related_name='specifications',
        on_delete=models.CASCADE,
        verbose_name="Sản phẩm"
    )

    key = models.CharField(
        max_length=100, verbose_name="Thuộc tính (ví dụ: Màn hình, Chip xử lý)")
    value = models.CharField(
        max_length=255, verbose_name="Giá trị (ví dụ: OLED 6.5 inches, Apple A13 Bionic)")
    order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")

    class Meta:
        verbose_name = "Thông số kỹ thuật"
        verbose_name_plural = "Thông số kỹ thuật"
        ordering = ['product', 'order']  # Sắp xếp theo sản phẩm và thứ tự

    def __str__(self):
        return f"{self.product.name} - {self.key}: {self.value}"


class News(models.Model):
    # Tiêu đề tin tức (tương ứng với <h3>)
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")

    # Tóm tắt/Nội dung ngắn gọn (tương ứng với <p> nội dung)
    summary = models.TextField(verbose_name="Tóm tắt nội dung")

    # Ngày đăng tin (tương ứng với 'Ngày:')
    # auto_now_add=True sẽ tự động điền ngày khi tin tức được tạo lần đầu
    published_date = models.DateTimeField(
        default=timezone.now, verbose_name="Ngày đăng")

    # Nguồn tin (tương ứng với 'Nguồn:')
    source = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Nguồn tin")

    # Hình ảnh (tương ứng với <img src=...>)
    image = models.ImageField(
        upload_to='news_images/', verbose_name="Hình ảnh")

    # Đường dẫn liên kết (tương ứng với <a href=...>)
    external_link = models.URLField(
        max_length=500, blank=True, null=True, verbose_name="Đường dẫn Đọc thêm")

    # Trường tùy chọn để đánh dấu tin tức đặc biệt (ví dụ: 'store-info')
    is_store_info = models.BooleanField(
        default=False, verbose_name="Là thông tin cửa hàng")

    class Meta:
        verbose_name = "Tin tức"
        verbose_name_plural = "Tin tức & Cập nhật"
        # Sắp xếp tin tức mới nhất lên đầu
        ordering = ['-published_date']

    def __str__(self):
        return self.title
