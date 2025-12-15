from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product, Category

# Create your views here.


def index(request):
    return render(request, 'index.html')


def cart(request):
    return render(request, 'cart.html')


def checkout(request):
    return render(request, 'checkout.html')


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
    return redirect('category', slug='accessory')


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    qs = Product.objects.filter(available=True, category__slug=slug)

    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    storage = request.GET.get('storage', '').strip()
    if storage:
        qs = qs.filter(Q(name__icontains=storage) | Q(description__icontains=storage))

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
    context = {'products': products, 'category': category, 'q': q, 'storage': storage, 'sort': sort}
    return render(request, 'category.html', context)


def response(request):
    return render(request, 'response.html')
