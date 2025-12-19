from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Cart, CartItem, Order, OrderItem, SavedDesign
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import razorpay # Added for Payment Gateway

# Helper to get user cart
def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id: request.session.create(); session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

# AI Trigger (Placeholder)
@user_passes_test(lambda u: u.is_superuser)
def trigger_ai(request):
    return HttpResponse("<h1>🤖 AI is Sleeping (Code coming soon)</h1>")

# Product Views
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

# Cart Actions
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

def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('checkout')

# --- CHECKOUT & PAYMENT LOGIC (UPDATED) ---
def checkout_view(request):
    cart = _get_cart(request)
    if cart.items.count() == 0: 
        return redirect('home')
    
    # 1. Calculate Real Total Amount from Cart
    total_amount = int(cart.total_price) 
    
    # 2. Razorpay Order Create
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment_data = {
            "amount": total_amount * 100,  # Amount in Paise
            "currency": "INR",
            "payment_capture": 1
        }
        order = client.order.create(data=payment_data)
        
        razorpay_order_id = order['id']
    except Exception as e:
        # Fallback if Razorpay fails (e.g. invalid keys)
        print(f"Razorpay Error: {e}")
        razorpay_order_id = "test_order_id"

    context = {
        'cart': cart,
        'cart_count': cart.items.count(),
        'total_amount': total_amount,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'currency': 'INR',
        'callback_url': '/order-success/' 
    }
    
    return render(request, 'store/checkout.html', context)

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
        return redirect('order_success_view')
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
def custom_design_view(request): 
    return render(request, 'store/custom_design.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): login(request, form.get_user()); return redirect('home')
    return render(request, 'store/login.html', {'form': AuthenticationForm()})

def logout_view(request): 
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): user = form.save(); login(request, user); return redirect('home')
    return render(request, 'store/register.html', {'form': UserCreationForm()})
def switch_currency(request, currency_code):
    # Allow all major currencies
    valid_currencies = ['INR', 'USD', 'EUR', 'GBP', 'AED', 'SAR', 'CAD', 'AUD']
    
    if currency_code in valid_currencies:
        request.session['currency'] = currency_code
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Order, Product

@staff_member_required
def owner_dashboard(request):
    # 1. Order Status Counts
    # 'status' field irukurathaala idhu work aagum
    pending_orders = Order.objects.filter(status='Pending').count()
    printed_orders = Order.objects.filter(status='Printed').count()
    shipped_orders = Order.objects.filter(status='Shipped').count()

    # 2. Financials (Fixed Error Here)
    # total_price -> total_amount (Database field name padi maaththeeruken)
    revenue_data = Order.objects.aggregate(Sum('total_amount'))
    total_revenue = revenue_data['total_amount__sum'] or 0
    
    # 3. Profit Calculation (Safe Mode)
    # Order-la 'product' field illa, so 'items' loop pannanum.
    # Oru vela loop fail aanalum crash aagama irukka 'try-except' potturuken.
    total_cost = 0
    try:
        orders = Order.objects.prefetch_related('items').all() # 'items' connection load pannum
        for order in orders:
            # Unga OrderItem model-la 'product' link irundha idhu work aagum
            for item in order.items.all():
                if hasattr(item, 'product') and item.product.cost_price:
                    total_cost += item.product.cost_price * item.quantity
    except Exception as e:
        # Loop fail aana, simple-ah 70% cost nu assume pannikalam (Temporary fix)
        total_cost = total_revenue * 0.70

    total_profit = total_revenue - total_cost

    # 4. Low Balance Alerts
    alerts = []
    if total_profit < 2000:
        alerts.append("⚠️ Low Wallet Balance! Recharge Printrove.")
    
    # 5. Top Selling Designs
    top_products = Product.objects.filter(is_bestseller=True)[:5]

    context = {
        'pending': pending_orders,
        'printed': printed_orders,
        'shipped': shipped_orders,
        'revenue': round(total_revenue, 2),
        'profit': round(total_profit, 2),
        'alerts': alerts,
        'top_products': top_products,
    }
    return render(request, 'admin/owner_dashboard.html', context)
from .models import Category

def home(request):
    categories = Category.objects.all() # Ella categories-ayum edukkom
    return render(request, 'index.html', {'categories': categories})
from .models import Product, Category, HomeBanner # HomeBanner import pannunga

def home(request):
    # Fetch Banners based on position
    main_banner = HomeBanner.objects.filter(position='main').first()
    side_top = HomeBanner.objects.filter(position='side_top').first()
    side_bottom = HomeBanner.objects.filter(position='side_bottom').first()
    
    categories = Category.objects.all()
    products = Product.objects.all()
    
    context = {
        'main_banner': main_banner,
        'side_top': side_top,
        'side_bottom': side_bottom,
        'categories': categories,
        'products': products
    }
    return render(request, 'index.html', context)
def home(request):
    # 'prefetch_related' use panrom, idhu subcategories-a fast-a edukum
    categories = Category.objects.prefetch_related('subcategories').all()
    
    products = Product.objects.filter(is_approved=True)
    
    # ... (Mattha logic apdiye irukattum like cart, etc.) ...

    context = {
        'categories': categories,
        'products': products,
        # ... matha context variables ...
    }
    return render(request, 'index.html', context)