from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('new/', views.new, name='new'),
    path('contact/', views.contact, name='contact'),
    path('iphone/', views.iphone, name='iphone'),
    path('ipad/', views.ipad, name='ipad'),
    path('macbook/', views.macbook, name='macbook'),
    path('phu-kien/', views.phukien, name='phukien'),
    path('response/', views.response, name='response'),
    path('payment/', views.payment, name='payment'),
    path('product_detail/<slug:product_slug>/',
         views.product_detail, name='product_detail'),
    # URL cho Đăng ký
    path('signup/', views.signup, name='signup'),

    # URL cho Đăng nhập
    path('login/', views.login, name='login'),

    # URL cho Đăng xuất
    path('logout/', views.logout_view, name='logout'),
]
