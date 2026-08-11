from django.urls import path, include
from . import views

app_name = 'store' 

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    #signup
    path('signup/', views.signup_view, name='signup'),

    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),

    #adjusting and deleting items
    path('cart/increase/<int:book_id>/', views.update_cart_item, {'action': 'increase'}, name='increase_cart_item'),
    path('cart/decrease/<int:book_id>/', views.update_cart_item, {'action': 'decrease'}, name='decrease_cart_item'),
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_cart_item'),


]
