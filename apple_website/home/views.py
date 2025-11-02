from django.shortcuts import render, redirect

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
    return render(request, 'iphone.html')


def ipad(request):
    return render(request, 'ipad.html')


def macbook(request):
    return render(request, 'macbook.html')


def phukien(request):
    return render(request, 'phu-kien.html')


def response(request):
    return render(request, 'response.html')
