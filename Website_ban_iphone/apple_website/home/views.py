from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product, ProductVariant, Category
from django.views.decorators.http import require_POST

# Create your views here.


def index(request):
    return render(request, 'index.html')


def cart(request):
    # cart keys stored as "productid:variantid" => qty
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for key, qty in cart.items():
        try:
            pid, vid = key.split(':')
        except ValueError:
            pid, vid = key, '0'
        try:
            p = Product.objects.get(pk=int(pid))
        except Product.DoesNotExist:
            continue
        variant = None
        price = float(p.price)
        if vid and vid != '0':
            try:
                variant = ProductVariant.objects.get(pk=int(vid), product=p)
                price = float(variant.price)
            except ProductVariant.DoesNotExist:
                variant = None
        subtotal = price * int(qty)
        items.append({'product': p, 'variant': variant, 'qty': int(qty), 'subtotal': subtotal, 'key': key})
        total += subtotal
    return render(request, 'cart.html', {'cart_items': items, 'cart_total': total})


def checkout(request):
    if request.method == 'POST':
        # simple checkout: clear cart and show response
        request.session['cart'] = {}
        return redirect('response')
    # show checkout summary
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for key, qty in cart.items():
        try:
            pid, vid = key.split(':')
        except ValueError:
            pid, vid = key, '0'
        try:
            p = Product.objects.get(pk=int(pid))
        except Product.DoesNotExist:
            continue
        variant = None
        price = float(p.price)
        if vid and vid != '0':
            try:
                variant = ProductVariant.objects.get(pk=int(vid), product=p)
                price = float(variant.price)
            except ProductVariant.DoesNotExist:
                variant = None
        subtotal = price * int(qty)
        items.append({'product': p, 'variant': variant, 'qty': int(qty), 'subtotal': subtotal})
        total += subtotal
    return render(request, 'checkout.html', {'cart_items': items, 'cart_total': total})


def new(request):
    return render(request, 'new.html')


def contact(request):
    return render(request, 'contact.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def iphone(request):
    return redirect('category', slug='iphone')


def ipad(request):
    return redirect('category', slug='ipad')


def macbook(request):
    return redirect('category', slug='macbook')


def phukien(request):
    # category slug for accessories in DB is 'accessory'
    return redirect('category', slug='accessory')


def category(request, slug):
    # Generic category view: render products for any category slug
    category = get_object_or_404(Category, slug=slug)
    qs = Product.objects.filter(available=True, category__slug=slug)

    # search
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # storage filter (match variant names or product name/description)
    storage = request.GET.get('storage', '').strip()
    if storage:
        variant_product_ids = ProductVariant.objects.filter(product__category__slug=slug, name__icontains=storage).values_list('product_id', flat=True)
        qs = qs.filter(Q(pk__in=variant_product_ids) | Q(name__icontains=storage) | Q(description__icontains=storage))

    # sort
    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        qs = qs.order_by('price')
    elif sort == 'price_desc':
        qs = qs.order_by('-price')

    products = list(qs)
    for p in products:
        try:
            p.discount_percent = int(((p.old_price - p.price) / p.old_price) * 100) if p.old_price else 0
        except Exception:
            p.discount_percent = 0

    context = {
        'products': products,
        'category': category,
        'q': q,
        'storage': storage,
        'sort': sort,
    }
    return render(request, 'category.html', context)


def response(request):
    return render(request, 'response.html')


def payment(request):
    return render(request, 'payment.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    variants = product.variants.all()
    # pick a default variant (explicit or first)
    default_variant = variants.filter(is_default=True).first() or (variants.first() if variants.exists() else None)
    # price shown is variant price if exists else product.price
    if default_variant:
        display_price = default_variant.price
    else:
        display_price = product.price
    try:
        product.discount_percent = int(((product.old_price - display_price) / product.old_price) * 100) if product.old_price else 0
    except Exception:
        product.discount_percent = 0
    return render(request, 'product-detail.html', {'product': product, 'variants': variants, 'default_variant': default_variant, 'display_price': display_price})


@require_POST
def add_to_cart(request, product_id):
    qty = int(request.POST.get('qty', 1))
    variant_id = request.POST.get('variant_id') or '0'
    key = f"{product_id}:{variant_id}"
    cart = request.session.get('cart', {})
    cart[key] = cart.get(key, 0) + qty
    request.session['cart'] = cart
    return redirect('cart')


@require_POST
def remove_from_cart(request, product_id):
    variant_id = request.POST.get('variant_id') or '0'
    key = f"{product_id}:{variant_id}"
    cart = request.session.get('cart', {})
    cart.pop(key, None)
    request.session['cart'] = cart
    return redirect('cart')


@require_POST
def update_cart(request):
    # expects POST data names like qty_<productid>_<variantid>=n
    cart = request.session.get('cart', {})
    for key, val in request.POST.items():
        if key.startswith('qty_'):
            pid_vid = key.split('qty_', 1)[1]
            try:
                q = int(val)
            except Exception:
                q = 0
            if q <= 0:
                cart.pop(pid_vid, None)
            else:
                cart[pid_vid] = q
    request.session['cart'] = cart
    return redirect('cart')


def product_detail_redirect(request):
    # Legacy templates linked to 'product_detail' without slug.
    # Redirect to product listing (iphone) to avoid NoReverseMatch.
    return redirect('iphone')
