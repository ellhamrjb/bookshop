from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Book, Cart, CartItem


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



def add_to_cart(request, book_id):
    book =get_object_or_404(Book, id=book_id, is_available=True)

    if request.user.is_authenticated: #login
        cart, created=Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        #not login
        cart = request.session.get('cart', {})
        book_id_str = str(book_id)
        if book_id_str in cart:
            cart[book_id_str] += 1
        else:
            cart[book_id_str] = 1
        request.session['cart'] = cart

    return redirect('store:book_detail', slug=book.slug)

def cart_detail(request):
    cart_items = []
    total_price = 0

    if request.user.is_authenticated:
        #show by database
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = cart.items.all()
            total_price = sum(item.get_total_price() for item in cart_items)
    else:
        # show by session
        session_cart = request.session.get('cart', {})
        for b_id, quantity in session_cart.items():
            book = Book.objects.get(id=int(b_id))
            item_total = book.price * quantity 
            total_price += item_total
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'price': book.price,
                'total_item_price': item_total              })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/cart_detail.html', context)



def update_cart_item(request, book_id, action):
    #adjusting items
    book= get_object_or_404(Book, id=book_id)

    if request.user.is_authenticated:
        #loggined users
        cart, _=Cart.objects.get_or_create(user=request.user)
        item=CartItem.objects.filter(cart=cart,book=book).first()

        if item:
            if action=='increase':
                item.quantity+=1
            elif action=='decrease':
                item.quantity-=1


            #for item=0
            if item.quantity<1:
                item.delete()
            else:
                item.save()
    else:
        #not loggined users
        cart=request.sessio.get('cart',{})
        key=str(book_id)

        if key in cart:
            if action=='increase':
                cart[key]+=1
            elif action=='decrease':
                cart[key]-=1

            #item=0
            if cart[key]<1:
                del cart[key]

        request.session['cart']=cart
        request.session.modified=True

    return redirect('store:cart_detail')


def remove_from_cart(request,book_id):
    #Completely delete an item

    if request.user.is_authenticated:
        cart,_=Cart.objects.get_or_create(user=request.user)
        CartItem.objects.filter(cart=cart,book_id=book_id).delete()

    else:
        cart = request.session.get('cart',{})
        cart.pop(str(book_id),None)
        request.session['cart']=cart
        request.session.modified=True

    return redirect('store:cart_detail')
            

