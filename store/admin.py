from django.contrib import admin
from.models import Category, Book, CustomUser
from django.contrib.auth.admin import UserAdmin


admin.site.register(CustomUser,UserAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)} #auto-fills the slug from the title when I type in the admin


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "price", "stock", "is_available"]
    list_filter = ["category", "is_available"]
    search_fields = ["title", "author"]
    prepopulated_fields = {"slug": ("title",)}