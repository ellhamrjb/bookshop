from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'store' 

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    

    #signup
    path('signup/', views.signup_view, name='signup'), 
    #path('signup/', views.signup, name='signup'),
    #login
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    #logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),



    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),

    #adjusting and deleting items
    path('cart/increase/<int:book_id>/', views.update_cart_item, {'action': 'increase'}, name='increase_cart_item'),
    path('cart/decrease/<int:book_id>/', views.update_cart_item, {'action': 'decrease'}, name='decrease_cart_item'),
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_cart_item'),



    #payments
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment_start, name='payment_start'),
    path('payment/<int:order_id>/verify/', views.payment_verify, name='payment_verify'),

    #order history
    path('orders/', views.order_history, name='order_history'),

    #order detail
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]
