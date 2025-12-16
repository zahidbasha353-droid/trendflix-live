from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Cart, CartItem, Order, OrderItem, SavedDesign, Category
from .forms import ProductUploadForm
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Count
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import razorpay

print("✅ SUPER VIEWS.PY LOADED SUCCESSFULLY!")

# ==========================================
# 🏭 AUTOMATION CONFIGURATION (Simple)
# ==========================================
# (Tokens are assumed to be correct from your old code)

def send_order_to_printrove(order):
    print(f"🔄 [Printrove] Processing Order #{order.id}...")
    # (Simplified for now - just saves status)
    order.supplier_name = "Printrove"
    order.save()
    return True

def send_order_to_printify(order):
    print(f"✈️ [Printify] Processing Order #{order.id}...")
    order.supplier_name = "Printify"
    order.save()
    return True

# ==========================================
# 🛍️ STORE VIEWS
# ==========================================

def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id: request.session.create(); session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def home(request):
    # FIXED: 'is_active' used instead of 'is_approved'
    products = Product.objects.filter(is_active=True).order_by('-created')
    cart = _get_cart(request)
    return render(request, 'store/home.html', {'products': products, 'cart_count': cart.items.count()})

def product_detail(request, slug):
    # FIXED: Uses 'slug' instead of 'product_id'
    product = get_object_or_404(Product, slug=slug, is_active=True)
    cart = _get_cart(request)
    return render(request, 'store/product_detail.html', {'product': product, 'cart_count': cart.items.count()})

def cart_view(request):
    cart = _get_cart(request)
    return render(request, 'store/cart.html', {'cart': cart, 'cart_count': cart.items.count()})

def add_to_cart(request, slug): # Changed product_id to slug
    product = get_object_or_404(Product, slug=slug)
    cart = _get_cart(request)
    
    # Simple Add Logic
    size = request.POST.get('size', 'M')
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
    if not created: cart_item.quantity += 1
    cart_item.save()
    
    return redirect('cart')

def remove_from_cart(request, item_id):
    get_object_or_404(CartItem, id=item_id).delete()
    return redirect('cart')

def checkout_view(request):
    cart = _get_cart(request)
    if cart.items.count() == 0: return redirect('home')
    
    # Razorpay Logic
    total_amount = int(cart.total_price * 100)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount': total_amount, 'currency': 'INR', 'payment_capture': '1'})
    
    return render(request, 'store/checkout.html', {
        'cart': cart, 
        'cart_count': cart.items.count(), 
        'razorpay_order_id': payment['id'], 
        'razorpay_key_id': settings.RAZORPAY_KEY_ID, 
        'total_price': cart.total_price, 
        'amount_paise': total_amount
    })

@csrf_exempt
def order_success_view(request):
    if request.method == "POST":
        cart = _get_cart(request)
        
        # Create Order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=request.POST.get('full_name', 'Guest'),
            address=request.POST.get('address', 'Online Payment'),
            city=request.POST.get('city', 'India'),
            state=request.POST.get('state', 'TN'),
            country="India",
            zipcode=request.POST.get('zipcode', '000000'),
            phone=request.POST.get('phone', '9999999999'),
            total_amount=cart.total_price, 
            status="Processing"
        )
        
        # Move items to Order
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, price=item.product.price, quantity=item.quantity)
        
        cart.items.all().delete() # Clear Cart

        # Automation Trigger
        send_order_to_printrove(order)

        return render(request, 'store/order_success.html')
    return redirect('home')

# --- AUTH & OTHER VIEWS ---

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): login(request, form.get_user()); return redirect('home')
    return render(request, 'store/login.html', {'form': AuthenticationForm()})

def logout_view(request):
    logout(request); return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): user = form.save(); login(request, user); return redirect('home')
    return render(request, 'store/register.html', {'form': UserCreationForm()})

# Design Lab
def design_lab(request):
    return render(request, 'store/design_lab.html')