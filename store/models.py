from django.db import models
from django.urls import reverse
from django.conf import settings 
from django.contrib.auth.models import User, AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True) #clean urls

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:category_detail", args=[self.slug])


class Book(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="books",
        on_delete=models.SET_NULL, # if we delete category we'll still have books
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    author = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:book_detail", args=[self.slug])

    @property
    def in_stock(self):
        return self.stock > 0



class Cart(models.Model):
    #for logins
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True,

    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username if self.user else 'Anonymous'}"

    @property
    def total_price(self):
        return sum(item.get_total_price() for item in self.items.all())



class CartItem(models.Model):
    #not logins
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name="items"
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

    def get_total_price(self):
        return self.book.price * self.quantity

