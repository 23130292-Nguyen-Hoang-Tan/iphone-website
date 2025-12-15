from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('new/', views.new, name='new'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('iphone/', views.iphone, name='iphone'),
    path('ipad/', views.ipad, name='ipad'),
    path('macbook/', views.macbook, name='macbook'),
    path('phu-kien/', views.phukien, name='phukien'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('response/', views.response, name='response'),
    path('payment/', views.payment, name='payment'),
    path('product_detail/', views.product_detail_redirect, name='product_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail_slug'),
]
