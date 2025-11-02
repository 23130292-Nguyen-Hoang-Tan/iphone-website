from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('new/', views.new, name='new'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('iphone/', views.iphone, name='iphone'),
    path('ipad/', views.ipad, name='ipad'),
    path('macbook/', views.macbook, name='macbook'),
    path('phu-kien/', views.phukien, name='phukien'),
    path('response/', views.response, name='response'),
]
