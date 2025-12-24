from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Product, Purchase
from .forms import SignUpForm


# Home page
def home_view(request):
    return render(request, 'e_commerce/home.html')


# Product list by category
def product_list(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'e_commerce/product_list.html', {
        'products': products,
        'category': category
    })


# Sign up / Login view
def signin_view(request):
     if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect('home')
     else:
      form = SignUpForm()

     return render(request, 'e_commerce/sign_in.html', {'form': form})


# Cart page
@login_required
def cart_view(request):
    cart_items = Purchase.objects.filter(user=request.user)

    for item in cart_items:
        item.subtotal = item.product.price * item.quantity

    cart_total = sum([item.subtotal for item in cart_items])

    return render(request, 'e_commerce/cart.html', {
        'cart_items': cart_items,
        'cart_count': cart_items.count(),
        'cart_total': cart_total,
    })


# Add to cart
@login_required
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    purchase, created = Purchase.objects.get_or_create(user=request.user, product=product)

    if not created:
        if purchase.quantity + 1 > product.stock:
            messages.error(request, f"Only {product.stock} units available for {product.name}.")
        else:
            purchase.quantity += 1
            purchase.save()
            messages.success(request, f"Added 1 {product.name} to your cart.")
    else:
        if product.stock < 1:
            messages.error(request, f"{product.name} is out of stock.")
        else:
            purchase.quantity = 1
            purchase.save()
            messages.success(request, f"Added {product.name} to your cart.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Checkout page
@login_required
def checkout_view(request):
    cart_items = Purchase.objects.filter(user=request.user)
    cart_total = sum([item.product.price * item.quantity for item in cart_items])

    if request.method == 'POST':
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(request, f"Not enough stock for {item.product.name}. Available: {item.product.stock}")
                return redirect('cart')

        for item in cart_items:
            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect('home')

    return render(request, 'e_commerce/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })


# Remove from cart
@login_required
def remove_from_cart(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user)
    purchase.delete()
    messages.success(request, f'{purchase.product.name} removed from your cart.')
    return redirect('cart')


# Context processor to get cart count globally
def cart_count(request):
    if request.user.is_authenticated:
        return {'cart_count': Purchase.objects.filter(user=request.user).count()}
    return {'cart_count': 0}

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        question = request.POST.get('question')
    return render(request, 'e_commerce/contactUs.html')
def shop_view(request):
    query = request.GET.get('q') 
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    return render(request, 'e_commerce/shop.html', {
        'products': products,
        'query': query,
    })

def signin_redirect(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'e_commerce/sign_in.html')


