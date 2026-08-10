from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Book 

class Command(BaseCommand):
    help = 'Seeds the database with initial categories and books'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to seed data...")

        
        categories = []
        for i in range(1, 11):
            cat_name = f"Category {i}"
            cat_slug = slugify(cat_name)
            category, created = Category.objects.get_or_create(name=cat_name, slug=cat_slug)
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Category: {cat_name}"))

        
        for i in range(1, 31):
            cat = categories[i % 10]
            book_title = f"Amazing Book {i}"
            book_slug = slugify(f"{book_title} {i}")
            
            book, created = Book.objects.get_or_create(
                slug=book_slug,
                defaults={
                    'category': cat,
                    'title': book_title,
                    'author': f"Author {i}",
                    'description': f"Description for book {i}",
                    'price': 10.50 + i,
                    'stock': 10 + i,
                    'is_available': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Book: {book_title}"))

        self.stdout.write(self.style.SUCCESS("Successfully seeded all data! 🎉"))
