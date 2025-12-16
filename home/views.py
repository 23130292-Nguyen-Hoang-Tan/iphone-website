from django.shortcuts import render, redirect, get_object_or_404
from . import views
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Product, Category, News

# Create your views here.


def index(request):
    return render(request, 'index.html')


def cart(request):
    return render(request, 'cart.html')


def checkout(request):
    return render(request, 'checkout.html')


def new(request):
    # Lấy tất cả tin tức, đã được sắp xếp theo ngày trong models.py (mới nhất trước)
    all_news = News.objects.all()

    # Truyền dữ liệu tin tức vào context để template có thể sử dụng
    context = {
        'news_items': all_news,
    }

    # Render template
    return render(request, 'new.html', context)


def contact(request):
    return render(request, 'contact.html')


def iphone(request):
    # Use case-insensitive lookup for category name to avoid casing issues from Admin
    iphone_category = Category.objects.filter(name__iexact='iPhone').first()
    if not iphone_category:
        products = Product.objects.none()
    else:
        products = Product.objects.filter(
            category=iphone_category).prefetch_related('variants')

    # 3. Truyền danh sách sản phẩm qua context để hiển thị trong template
    context = {
        'products': products
    }

    return render(request, 'iphone.html', context)


def ipad(request):
    # Use case-insensitive lookup for category name
    ipad_category = Category.objects.filter(name__iexact='iPad').first()
    if not ipad_category:
        products = Product.objects.none()
    else:
        products = Product.objects.filter(
            category=ipad_category).prefetch_related('variants')

    # 3. Truyền danh sách sản phẩm qua context
    context = {
        'products': products
    }

    return render(request, 'ipad.html', context)


def macbook(request):
    try:
        # 1. Tìm đối tượng Category có tên là 'Macbook' (case-insensitive)
        macbook_category = Category.objects.filter(
            name__iexact='Macbook').first()
        if not macbook_category:
            # No matching category found — return empty queryset
            products = Product.objects.none()
        else:
            # 2. Lấy TẤT CẢ sản phẩm (Product) thuộc danh mục đó
            # Dùng .prefetch_related('variants') để tối ưu truy vấn
            products = Product.objects.filter(
                category=macbook_category).prefetch_related('variants')

    except Category.DoesNotExist:
        # Xử lý trường hợp không tìm thấy danh mục 'Macbook'
        products = []

    # 3. Truyền danh sách sản phẩm qua context
    context = {
        'products': products
    }

    return render(request, 'macbook.html', context)


def phukien(request):
    # Use case-insensitive lookup for category name
    accessory_category = Category.objects.filter(
        name__iexact='phu kien').first()
    if not accessory_category:
        products = Product.objects.none()
    else:
        products = Product.objects.filter(
            category=accessory_category).prefetch_related('variants')

    # Pass products to template
    context = {
        'products': products
    }

    return render(request, 'phu-kien.html', context)


def response(request):
    return render(request, 'response.html')


def payment(request):
    return render(request, 'payment.html')


def product_detail(request, product_slug):
    # Lấy đối tượng Product dựa trên slug, nếu không tìm thấy thì trả về 404
    product = get_object_or_404(
        Product.objects.prefetch_related('variants', 'specifications'),
        slug=product_slug
    )

    # Lấy TẤT CẢ các biến thể (variants) của sản phẩm này (để chọn dung lượng/màu)
    variants = product.variants.all().order_by('storage', 'price')

    # Lấy các giá trị 'color' distinct từ queryset, và sau đó lấy các biến thể đầu tiên
    unique_colors_variants = variants.values('color').distinct()

    # Tái tạo danh sách biến thể chỉ chứa màu duy nhất (ví dụ: lấy biến thể đầu tiên của mỗi màu)
    # Đây là cách đơn giản để hiển thị button màu sắc
    unique_colors_list = []
    for item in unique_colors_variants:
        # Lấy biến thể đầu tiên cho màu đó
        v = variants.filter(color=item['color']).first()
        if v:
            unique_colors_list.append(v)

    # Lấy biến thể mặc định (ví dụ: biến thể đầu tiên) để hiển thị ban đầu
    default_variant = variants.first()

    # Lấy thông số kỹ thuật (specifications)
    specs = product.specifications.all()

    context = {
        'product': product,
        'variants': variants,
        'unique_colors': unique_colors_list,
        'default_variant': default_variant,  # Biến thể mặc định hiển thị
        'specs': specs,
    }

    return render(request, 'product-detail.html', context)

# --- 1. Logic ĐĂNG KÝ (Sign Up) ---


def signup(request):
    if request.method == 'POST':
        # SỬ DỤNG CustomUserCreationForm
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Django sẽ tự động lưu trường email.

            # Tự động đăng nhập người dùng sau khi đăng ký thành công
            login(request, user)
            return redirect('index')  # Chuyển hướng về trang chính
        # Nếu form không hợp lệ, nó sẽ trả lại form với các thông báo lỗi (bao gồm lỗi email)
    else:
        # Khi người dùng lần đầu truy cập trang (GET request)
        form = CustomUserCreationForm()  # SỬ DỤNG CustomUserCreationForm

    return render(request, 'signup.html', {'form': form})

# --- 2. Logic ĐĂNG NHẬP (Login) ---


def login(request):
    if request.method == 'POST':
        # AuthenticationForm chỉ cần username và password để xác thực
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Lấy đối tượng người dùng đã xác thực
            user = form.get_user()
            # Thiết lập session cho người dùng (Giữ người dùng đã đăng nhập)
            login(request, user)
            # Chuyển hướng về trang chính sau khi đăng nhập
            return redirect('index')
        else:
            # Nếu xác thực thất bại, nó sẽ trả lại form với lỗi chung
            pass
    else:
        # Khi người dùng lần đầu truy cập trang (GET request)
        form = AuthenticationForm()

    # Render (hiển thị) trang login.html cùng với đối tượng form
    return render(request, 'login.html', {'form': form})


# --- 3. Logic ĐĂNG XUẤT (Logout) ---
# Thường chỉ cần một hàm đơn giản để gọi logout
def logout_view(request):
    logout(request)  # Xóa session
    return redirect('login')  # Chuyển hướng về trang Đăng nhập
