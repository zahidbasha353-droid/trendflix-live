from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Cart, CartItem, Order, OrderItem, SavedDesign
# from .forms import ProductUploadForm  <-- TEMPORARY DISABLED
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
# import razorpay <-- TEMPORARY DISABLED (Settings la key podanum)
# from .utils import generate_print_manifest, push_to_supplier <-- TEMPORARY DISABLED
# from .ai_brain import run_ai_optimization  <-- TEMPORARY DISABLED

def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id: request.session.create(); session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

@user_passes_test(lambda u: u.is_superuser)
def trigger_ai(request):
    # report = run_ai_optimization()
    return HttpResponse("<h1>🤖 AI is Sleeping (Code coming soon)</h1>")

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.view_count += 1
    product.save()
    cart = _get_cart(request)
    return render(request, 'store/product_detail.html', {'product': product, 'cart_count': cart.items.count()})

def home(request):
    products = Product.objects.filter(is_approved=True).order_by('-is_trending', '-created_at')
    cart = _get_cart(request)
    return render(request, 'store/home.html', {'products': products, 'cart_count': cart.items.count()})

def cart_view(request):
    cart = _get_cart(request)
    return render(request, 'store/cart.html', {'cart': cart, 'cart_count': cart.items.count()})

def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart = _get_cart(request)
        size = request.POST.get('size', 'M')
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
        if not created: cart_item.quantity += 1
        cart_item.save()
        return redirect('cart')
    return redirect('home')

def remove_from_cart(request, item_id):
    get_object_or_404(CartItem, id=item_id).delete()
    return redirect('cart')

def checkout_view(request):
    cart = _get_cart(request)
    if cart.items.count() == 0: return redirect('home')
    # Dummy Razorpay setup for now to prevent crash
    return render(request, 'store/checkout.html', {'cart': cart, 'cart_count': cart.items.count(), 'total_price': cart.total_price})

def place_cod_order(request):
    if request.method == "POST":
        cart = _get_cart(request)
        if cart.items.count() == 0: return redirect('home')
        total_qty = sum(item.quantity for item in cart.items.all())
        is_bulk = True if total_qty >= 10 else False
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=request.POST.get('full_name'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zipcode=request.POST.get('zipcode'),
            phone=request.POST.get('phone'),
            total_amount=cart.total_price,
            status="Processing",
            is_bulk_order=is_bulk
        )
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, price=item.price, quantity=item.quantity)
        cart.items.all().delete()
        return render(request, 'store/order_success.html')
    return redirect('checkout')

def order_success_view(request):
    return render(request, 'store/order_success.html')

# MARKETPLACE & DASHBOARD
@login_required
def upload_design(request):
    return HttpResponse("Upload Design Page (Needs Forms.py)")

@login_required
def designer_dashboard(request):
    return HttpResponse("Designer Dashboard (Coming Soon)")

def owner_dashboard(request):
    return HttpResponse("Owner Dashboard (Coming Soon)")

# CUSTOM & AUTH
def custom_design_view(request): return render(request, 'store/custom_design.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): login(request, form.get_user()); return redirect('home')
    return render(request, 'store/login.html', {'form': AuthenticationForm()})

def logout_view(request): logout(request); return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): user = form.save(); login(request, user); return redirect('home')
    return render(request, 'store/register.html', {'form': UserCreationForm()})
# Itha store/views.py oda kadaisiya podunga

def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    # Add item to cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    # Direct ah checkout page ku pogum
    return redirect('checkout')
# store/views.py la last line-a idha podunga

def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('checkout')