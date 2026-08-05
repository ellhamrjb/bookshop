from django.urls import path, include
from . import views

app_name = 'store' 

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),


]
