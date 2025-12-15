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

    path('pay', views.index, name='index'),
    path('payment',views.payment, name='payment'),
    path('payment_ipn',views.payment_ipn, name='payment_ipn'),
    path('payment_return', views.payment_return, name='payment_return'),
    path('query',views.query, name='query'),
    path('refund',views.refund, name='refund'),
    #path('^admin/', admin.site.urls),
]
