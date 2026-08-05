from django.shortcuts import render, get_object_or_404
from .models import Category, Book


def home(request):
    featured_books= Book.objects.filter(is_available=True)[:8]
    categories= Category.objects.all()
    context={
        "featured_books": featured_books,
        "categories": categories,
    }
    return render (request,'store/home.html', context)



def book_list(request):
    books = Book.objects.filter(is_available=True)
    categories = Category.objects.all()

    category_slug = request.GET.get("category")
    if category_slug:
        books = books.filter(category__slug=category_slug)

    query = request.GET.get("q")
    if query:
        books = books.filter(title__icontains=query)  #case-insensitive "contains" search, like "harry" matches "Harry Potter

    context = {
        "books": books,
        "categories": categories,
        "selected_category": category_slug,
        "query": query or "",
    }
    return render(request, "store/book_list.html", context)



def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, is_available=True)
    related_books = (
        Book.objects.filter(category=book.category, is_available=True)
        .exclude(id=book.id)[:4]
    )
    context = {
        "book": book,
        "related_books": related_books,
    }
    return render(request, "store/book_detail.html", context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category, is_available=True)
    categories = Category.objects.all()
    context = {
        "category": category,
        "books": books,
        "categories": categories,
    }
    return render(request, "store/category_detail.html", context)