from django.shortcuts import render, redirect
from .models import Pizza, Cart, CartItem
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Home Page
def home(request):
    if request.user.is_authenticated:
        return redirect('menu')  # Redirect logged-in users to menu
    return render(request, 'home.html')  # Show home page for unauthenticated users


# Login Page
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = authenticate(username=username, password=password)
        if user_obj is None:
            messages.error(request, 'User not found or incorrect credentials')
            return redirect('login')

        login(request, user_obj)
        messages.success(request, 'Login successful')
        return redirect('menu')  # Redirect to menu after login

    return render(request, 'login.html')

# Register Page
def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')

            # Create new user
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()

            messages.success(request, 'Account created successfully')
            return redirect('login')

        except Exception as e:
            messages.error(request, 'Something went wrong')
            return redirect('signup')

    return render(request, 'signup.html')

# Add to Cart
@login_required(login_url='login')
def add_cart(request, pizza_uid):
    user = request.user
    try:
        pizza_obj = Pizza.objects.get(uid=pizza_uid)
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
        CartItem.objects.create(cart=cart, pizza=pizza_obj)
        messages.success(request, 'Item added to cart successfully')
    except Pizza.DoesNotExist:
        messages.error(request, 'Pizza not found')
    except Exception as e:
        messages.error(request, 'An error occurred while adding to cart')

    return redirect('menu')  # Redirect back to the menu

# Cart View
@login_required(login_url='login')
def cart(request):
    try:
        cart = Cart.objects.get(is_paid=False, user=request.user)
        context = {'cart': cart}
    except Cart.DoesNotExist:
        context = {'cart': None}
        messages.info(request, 'Your cart is empty')
    
    return render(request, 'cart.html', context)

# Orders Page
@login_required(login_url='login')
def orders(request):
    orders = Cart.objects.filter(is_paid=True, user=request.user)
    context = {'orders': orders}
    return render(request, 'orders.html', context)

# Remove Cart Item
@login_required(login_url='login')
def remove_cart_items(request, cart_item_uid):
    try:
        CartItem.objects.get(uid=cart_item_uid).delete()
        messages.success(request, 'Item removed from cart')
    except CartItem.DoesNotExist:
        messages.error(request, 'Cart item not found')
    except Exception as e:
        messages.error(request, 'An error occurred while removing item from cart')

    return redirect('cart')

# Menu Page
@login_required(login_url='login')
def menu(request):
    pizzas = Pizza.objects.all()
    return render(request, 'menu.html', {'pizzas': pizzas})

@login_required(login_url='login')
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user, is_paid=False)
        cart.is_paid = True
        cart.save()
        messages.success(request, "Order placed successfully!")
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty or the order has already been placed.")
    
    return redirect('orders')  # Redirect to orders page after checkout
