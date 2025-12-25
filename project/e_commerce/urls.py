from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/<slug:category>/', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:purchase_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.custom_login_view, name='login'),
    path('contact/', views.contact_view, name='contact'),
    path('shop/', views.shop_view, name='shop'),
    path('signin/', views.signin_redirect, name='logout'),
    path('orders/', views.order_history, name='order_history'),

]
