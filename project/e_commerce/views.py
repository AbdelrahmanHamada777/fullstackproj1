from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import transaction

from .models import Product, Purchase, Order, OrderItem
from .forms import SignUpForm


# Home page
def home_view(request):
    # Get the cheapest product from each category for "Hot Sales"
    categories = ['Monitors', 'Graphics_Cards', 'Processors', 'Cases']
    hot_sales = []
    
    for category in categories:
        cheapest = Product.objects.filter(category=category).order_by('price').first()
        if cheapest:
            hot_sales.append(cheapest)
    
    return render(request, 'e_commerce/home.html', {'hot_sales': hot_sales})


# Product list by category
def product_list(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'e_commerce/product_list.html', {
        'products': products,
        'category': category
    })


# Sign up / Login view
def signup_view(request):
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

     return render(request, 'e_commerce/signup.html', {'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'e_commerce/login.html', {'form': form})


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
    
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        
    cart_total = sum([item.subtotal for item in cart_items])

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')

        if not address or not phone or not zip_code:
            messages.error(request, "Please fill in all shipping details.")
            return redirect('checkout')

        try:
            with transaction.atomic():
                # Create the Order record
                order = Order.objects.create(
                    user=request.user,
                    address=address,
                    phone=phone,
                    zip_code=zip_code,
                    total_price=cart_total
                )

                # Re-fetch items with select_for_update to lock rows and get latest stock
                for item in cart_items:
                    # Lock the product row
                    product = Product.objects.select_for_update().get(id=item.product.id)
                    
                    if item.quantity > product.stock:
                        # This raises an exception that will trigger a rollback
                        raise ValueError(f"Not enough stock for {product.name}. Available: {product.stock}")
                    
                    product.stock -= item.quantity
                    product.save()

                    # Create OrderItem record
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item.quantity,
                        price=product.price
                    )

                # Clear cart only if all updates succeed
                cart_items.delete()
                
            messages.success(request, "Order placed successfully!")
            return redirect('home')

        except ValueError as e:
            # Catch the specific error and notify user (transaction already rolled back)
            messages.error(request, str(e))
            return redirect('cart')

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
    return redirect('login')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items__product')
    return render(request, 'e_commerce/order_history.html', {'orders': orders})


