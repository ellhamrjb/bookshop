import os
import django
from django.utils.text import slugify
from store.models import Category, Book


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookshop.settings')
django.setup()

def seed_data():
    print('starting to seed data...')

    categories = []
    for i in range(1, 11):
        cat_name = f"Category {i}"
        cat_slug = slugify(cat_name)
        #for the duplicate error
        category, created = Category.objects.get_or_create(name=cat_name, slug=cat_slug)
        categories.append(category)
        print(f"Created Category: {cat_name}")


    for i in range(1, 31):  # 30 books
        cat = categories[i % 10]  
        book_title = f"Amazing Book {i}"
        book_slug = slugify(f"{book_title} {i}")



        book, created = Book.objects.get_or_create(
            slug=book_slug,
            defaults={
                'category': cat,
                'title': book_title,
                'author': f"Author {i}",
                'description': f"This is a great description for book {i}. It is very interesting!",
                'price': 10.50 + i,  # different prices
                'stock': 10 + i,
                'is_available': True,
            }
        )
        if created:
            print(f"Created Book: {book_title} in {cat.name}")

    print("Successfully seeded all data!")

if __name__ == "__main__":
    seed_data()
