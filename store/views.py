from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Count
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
import json
import razorpay

# Models Import
from .models import (
    Product, Category, SubCategory, HomeBanner, 
    Cart, CartItem, Order, OrderItem, SavedDesign, SiteSettings
)

# --- HELPER: GET USER CART ---
def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id: 
            request.session.create()
            session_id = request.session.session_key
        # Note: Inga models-la session_id field irukka nu check pannikonga
        cart, created = Cart.objects.get_or_create(user=None) 
    return cart

# --- HOME VIEW (BANNER + CATEGORY + PRODUCT) ---
def home(request):
    categories = Category.objects.all()
    banners = HomeBanner.objects.filter(is_active=True)
    
    # 1. Men's Top Deals section-kaga
    mens_deals = Product.objects.filter(category__name__icontains='Men', deal_type='top_deal')[:4]
    
    # 2. Women's Clearance section-kaga
    womens_clearance = Product.objects.filter(category__name__icontains='Women', deal_type='clearance')[:4]
    
    # 3. Best Sellers section-kaga
    best_sellers = Product.objects.filter(deal_type='best_seller')[:8]

    context = {
        'categories': categories,
        'banners': banners,
        'mens_deals': mens_deals,
        'womens_clearance': womens_clearance,
        'best_sellers': best_sellers,
    }
    return render(request, 'store/index.html', context)

# --- PRODUCT DETAIL ---
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # View count update (Model-la intha field irukanum)
    if hasattr(product, 'view_count'):
        product.view_count += 1
        product.save()
    
    cart = _get_cart(request)
    return render(request, 'store/product_detail.html', {
        'product': product, 
        'cart_count': cart.items.count()
    })

# --- CART ACTIONS ---
def cart_view(request):
    cart = _get_cart(request)
    return render(request, 'store/cart.html', {
        'cart': cart, 
        'cart_count': cart.items.count()
    })

def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart = _get_cart(request)
        size = request.POST.get('size', 'M')
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created: 
            cart_item.quantity += 1
        cart_item.save()
        return redirect('cart_view')
    return redirect('home')

def remove_from_cart(request, item_id):
    get_object_or_404(CartItem, id=item_id).delete()
    return redirect('cart_view')

def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('checkout_view')

# --- CHECKOUT & RAZORPAY ---
def checkout_view(request):
    cart = _get_cart(request)
    if cart.items.count() == 0: 
        return redirect('home')
    
    total_amount = int(cart.total_price) 
    
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment_data = {
            "amount": total_amount * 100, # Paise
            "currency": "INR",
            "payment_capture": 1
        }
        order = client.order.create(data=payment_data)
        razorpay_order_id = order['id']
    except Exception as e:
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

# --- OWNER DASHBOARD ---
@staff_member_required
def owner_dashboard(request):
    pending_orders = Order.objects.filter(status='Pending').count()
    revenue_data = Order.objects.aggregate(Sum('total_amount'))
    total_revenue = revenue_data['total_amount__sum'] or 0
    
    # Quick Profit Calc (Revenue - Cost)
    total_cost = 0
    orders = Order.objects.prefetch_related('items__product').all()
    for order in orders:
        for item in order.items.all():
            if item.product.cost_price:
                total_cost += item.product.cost_price * item.quantity
    
    total_profit = total_revenue - total_cost

    context = {
        'pending': pending_orders,
        'revenue': round(total_revenue, 2),
        'profit': round(total_profit, 2),
        'top_products': Product.objects.filter(is_bestseller=True)[:5],
    }
    return render(request, 'admin/owner_dashboard.html', context)

# --- AUTH VIEWS ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            login(request, form.get_user())
            return redirect('home')
    return render(request, 'store/login.html', {'form': AuthenticationForm()})

def logout_view(request): 
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'store/register.html', {'form': UserCreationForm()})
# store/views.py

def order_success_view(request):
    """Order success aanathukku apram kaatta vendiya page"""
    return render(request, 'store/order_success.html')

def switch_currency(request, currency_code):
    """Currency mathurathukku (Optional - needed for your URL)"""
    valid_currencies = ['INR', 'USD', 'EUR', 'GBP', 'AED', 'SAR', 'CAD', 'AUD']
    if currency_code in valid_currencies:
        request.session['currency'] = currency_code
    return redirect(request.META.get('HTTP_REFERER', 'home'))
# store/views.py oda bottom-la idhai paste pannunga

def custom_design_view(request):
    """Custom Design page-ah load panna"""
    return render(request, 'store/custom_design.html')

def order_success_view(request):
    """Order success page-ah load panna"""
    return render(request, 'store/order_success.html')

def switch_currency(request, currency_code):
    """Currency mathurathukku"""
    valid_currencies = ['INR', 'USD', 'EUR', 'GBP', 'AED', 'SAR', 'CAD', 'AUD']
    if currency_code in valid_currencies:
        request.session['currency'] = currency_code
    return redirect(request.META.get('HTTP_REFERER', 'home'))
# store/views.py

@login_required
def designer_dashboard(request):
    """Designer Dashboard page placeholder"""
    return render(request, 'store/designer_dashboard.html')

@login_required
def upload_design(request):
    """Design upload page placeholder"""
    return render(request, 'store/upload_design.html')
# Views.py logic
mens_deals = Product.objects.filter(category__name='Men', deal_type='top_deal')[:4]
womens_clearance = Product.objects.filter(category__name='Women', deal_type='clearance')[:4]
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.shortcuts import redirect
from .models import Product, Category

def auto_update_products(request, category_name):
    # Category-ah kandupudikkiroam
    try:
        category = Category.objects.get(name__icontains=category_name)
    except Category.DoesNotExist:
        messages.error(request, f"Category '{category_name}' find panna mudiyala!")
        return redirect('/admin/store/product/')

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    # Amazon search URL (Category-padi search pannum)
    search_url = f"https://www.amazon.in/s?k={category_name}+deals"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all("div", {"data-component-type": "s-search-result"})

    count = 0
    for item in items[:30]: # Extra products check pandroam to get 20 clean ones
        if count >= 20: break
        
        try:
            name = item.h2.text.strip()
            price_span = item.find("span", "a-price-whole")
            price = float(price_span.text.replace(',', '').strip()) if price_span else 499.00
            
            img_tag = item.find("img", "s-image")
            img_url = img_tag['src'] if img_tag else ""

            link_tag = item.find("a", "a-link-normal")
            raw_url = "https://www.amazon.in" + link_tag['href']
            affiliate_url = f"{raw_url.split('?')[0]}?tag=zahidbasha-21"

            # 🚨 DUPLICATE CHECK: URL vachhu check pandroam
            product, created = Product.objects.get_or_create(
                amazon_url=raw_url,
                defaults={
                    'name': name[:200],
                    'category': category,
                    'image_url_path': img_url,
                    'selling_price': price,
                    'cost_price': price + 200, # Mock cost price for discount
                    'affiliate_link': affiliate_url,
                    'deal_type': 'top_deal',
                    'is_approved': True
                }
            )
            if created:
                count += 1
        except:
            continue

    messages.success(request, f"Success! {count} pudhu products '{category_name}' section-la update aayiduchi!")
    return redirect('/admin/store/product/')