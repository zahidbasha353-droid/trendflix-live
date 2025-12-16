from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Cart, CartItem, Order, OrderItem, SavedDesign
from .forms import ProductUploadForm
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Count, Avg, F
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import date
import json
import requests
import razorpay

from .ai_brain import run_ai_optimization

print("✅ NEW VIEWS.PY LOADED SUCCESSFULLY!") # இது வந்தா புது கோட் வேலை செய்யுதுனு அர்த்தம்

# ==========================================
# 🚀 AUTOMATION CONFIGURATION (API KEYS)
# ==========================================

# 1. PRINTROVE (INDIA)
PRINTROVE_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiNjJmNjEwY2ExM2MwNGZjNjE2MjlhOTVjZDk5ZWQzMjg4NmE1ZDYxMzU3OWE3ZjMxYWNmNjBmNGFhNTk1MDNiZDY2OWI0YWZmOTc0NTU4YTAiLCJpYXQiOjE3NjU4Nzc3MzguOTM2NzgsIm5iZiI6MTc2NTg3NzczOC45MzY3ODcsImV4cCI6MTc5NzQxMzczOC45Mjk2MzksInN1YiI6IjE3ODA0MiIsInNjb3BlcyI6W119.oGh3gAuCCEAM4tcSYZ9rLO5OgnUHMvHqqCunyJ3xXBJ-5nCQ5NjVTJ5DaF8ZilfdSf4Bro9xB85uIBOfaJ8bPjQeF1sg-Bjiy7o96NVXIXyclf0_2rnpSJdl5DKFIR6tf5jakRvdPUX1EgkiKtW5TPXzp96UV0IywwDwqvaK6wWWFEFUm5QlSNei5r5BTDQeQX9Zkhrx2nFvK8bfW9u-CG9vCNRJMz-bFqU1mdLg9KY0xdDVH3DwQqGiOtaL1SxplYchfeRq4rjBBGMvwFwXRUv61egleoBpJWBlx2iF_7U2pj7iDABcorQGRkvFftM8XazJL4Zn05afSvvHxVmoCEopAte5ZXZ1hwWbTM9j2yZIp_c3UmyvVM21n2d6UhOG4Kq_QZw2yrrxZALXvIy3DVNPWgBYln4Q-L0kFDsRBG24JYpJpmJwmwWG-aE59iUqluVQngC1QjTBk_yWqlAzHRy1pp6_55CBCD4BEbgdjIq6wJ_bibOB3trf28I-Ltu3OM4u_q97za5DtmaW2AV5Sc0hVG4hHoOZbtNwTkbN2HODmGhw1sKIMhGb9eCZbTHsvr7mSadPy9OEN99wrTobhJhbmy70sdZrGKw6Ktb-ssfg5-qoAssuEJJUG8XEaBe83Umj6KsDN2m5QAh2cbhZE75MlRvzn515gMmWzQwTfWA"

# 2. PRINTIFY (GLOBAL)
PRINTIFY_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImI1NDM5Y2IzZjIyODUwOGQwMTk3NzUyYjYzOTIxNjI1NTNkZDMxMDQ1NGQxYWYxYWY2M2Q1ZTAwNmE3ZGFmYzQ3MGNmZjJjNTY2ODQzMjE3IiwiaWF0IjoxNzY1ODE5NDkwLjgyNjQ1NywibmJmIjoxNzY1ODE5NDkwLjgyNjQ1OCwiZXhwIjoxNzk3MzU1NDkwLjgxNjg1LCJzdWIiOiIyNTcxNjE3NyIsInNjb3BlcyI6WyJzaG9wcy5tYW5hZ2UiLCJzaG9wcy5yZWFkIiwiY2F0YWxvZy5yZWFkIiwib3JkZXJzLnJlYWQiLCJvcmRlcnMud3JpdGUiLCJwcm9kdWN0cy5yZWFkIiwicHJvZHVjdHMud3JpdGUiLCJ3ZWJob29rcy5yZWFkIiwid2ViaG9va3Mud3JpdGUiLCJ1cGxvYWRzLnJlYWQiLCJ1cGxvYWRzLndyaXRlIiwicHJpbnRfcHJvdmlkZXJzLnJlYWQiLCJ1c2VyLmluZm8iXX0.NYuRkmACFJI7dpxILoDjdj5-vrfId86sam5b2S5_l6fq9f54rt0vBQbZ75wzsO0vBX6VqhaE0cv-4J7yTMaDcvTtJeMRSJGuNTsA4_Nk6e6JXVn2ew0AZVm6Cpz1b7rkrrLXpL1FkNaIvWNNnEcj6lsTX_O_utDCZ0c3eyxltOjOZ-v6_vIKtSzu6zD_EQmKc9SwPArJ0ZyNMuwrIaPV2QszZ-d9s0CZGGD6hEfcvXoG2KcWjil-UGTTwZyjpDldY6mTr3FDJbjh2rHkCrCkayzaNDtbpQ-CNTiqR4QFhN2Jv3Rj-wI3Nvp1Jfue0zm491ZD6CPzNVGKCEJQ-0zGvX5khNFsfUQuTbI5pOI_BTRR4I9MFhgfqnNEaJmTMAaA0YE-NhUzYFBJAsIsZFhTuGGynjpXuur0WLcJSJuJFKELbgFCO8NK9XDkwA4Xc0c0k6DMusG59u5UPLogmSJHEI-H4JjY-Aut8ob4FNcPZMN2tLuq_GH2MSeqFk1X7o_w9YVIYCVoNxUgsN9cte2TmCBxiI8h6F0QfG4FiGNT1CH2W-HBCkaoCbN2QHn7yDp0e2W1yNOdefWF7hVN0ehugwygFbqpqdWObeLEkl6xStjk2V_JYoh5w4WpHZiHbYHXj4ccFTMl4umdEcv8WzCLVlHtvivtZfJUG9gmbWU34"
PRINTIFY_SHOP_ID = "25702412"

# ==========================================
# 🏭 AUTOMATION FUNCTIONS (API LOGIC)
# ==========================================

def send_order_to_printrove(order):
    print(f"🔄 [Printrove] Processing Order #{order.id}...")
    url = "https://api.printrove.com/api/external/orders"
    
    order_items = []
    for item in order.items.all():
        v_id = item.product.printrove_variant_id
        if v_id:
            order_items.append({"quantity": item.quantity, "variant_id": int(v_id), "is_plain": False})
    
    if not order_items:
        print("❌ [Printrove] No valid items found (Check Variant ID in Admin).")
        return False

    payload = {
        "reference_number": f"ORD-{order.id}",
        "retail_price": int(order.total_amount),
        "cod": False,
        "customer": {
            "name": order.full_name, "email": order.user.email if order.user else "guest@trendflix.com",
            "phone": order.phone, "address1": order.address, "city": order.city,
            "state": order.state, "pincode": order.zipcode, "country": "India"
        },
        "order_products": order_items
    }
    
    try:
        resp = requests.post(url, json=payload, headers={"Authorization": f"Bearer {PRINTROVE_TOKEN}", "Content-Type": "application/json"})
        order.api_response = f"Printrove: {resp.status_code} - {resp.text}"
        if resp.status_code in [200, 201]:
            data = resp.json()
            order.supplier_name = "Printrove"
            order.supplier_order_id = data.get('order_id') or data.get('id')
            order.save()
            print("✅ [Printrove] Order Sent Successfully!")
            return True
        else:
            print(f"❌ [Printrove] Failed: {resp.text}")
            order.save(); return False
    except Exception as e:
        print(f"⚠️ [Printrove] Error: {e}"); return False

def send_order_to_printify(order):
    print(f"✈️ [Printify] Processing Order #{order.id}...")
    url = f"https://api.printify.com/v1/shops/{PRINTIFY_SHOP_ID}/orders.json"
    
    line_items = []
    for item in order.items.all():
        if item.product.printify_product_id and item.product.printify_variant_id:
            line_items.append({"product_id": item.product.printify_product_id, "variant_id": int(item.product.printify_variant_id), "quantity": item.quantity})
    
    if not line_items:
        print("❌ [Printify] No valid items found (Check Product/Variant ID in Admin).")
        return False

    # Name Logic
    names = order.full_name.split()
    fname = names[0]; lname = names[-1] if len(names) > 1 else ""
    country_code = "IN" if order.country.lower() == "india" else "US"

    payload = {
        "external_id": f"ORD-{order.id}",
        "label": f"TrendFlix #{order.id}",
        "shipping_method": 1, "send_shipping_notification": True,
        "address_to": {
            "first_name": fname, "last_name": lname, "email": order.user.email if order.user else "guest@trendflix.com",
            "phone": order.phone, "country": country_code, "region": order.state,
            "address1": order.address, "city": order.city, "zip": order.zipcode
        },
        "line_items": line_items
    }
    
    try:
        resp = requests.post(url, json=payload, headers={"Authorization": f"Bearer {PRINTIFY_TOKEN}", "Content-Type": "application/json"})
        order.api_response = f"Printify: {resp.status_code} - {resp.text}"
        if resp.status_code == 200:
            data = resp.json()
            order.supplier_name = "Printify"
            order.supplier_order_id = data.get('id')
            order.save()
            print("✅ [Printify] Order Sent Successfully!")
            return True
        else:
            print(f"❌ [Printify] Failed: {resp.text}")
            order.save(); return False
    except Exception as e:
        print(f"⚠️ [Printify] Error: {e}"); return False

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

@user_passes_test(lambda u: u.is_superuser)
def trigger_ai(request):
    report = run_ai_optimization()
    return HttpResponse(f"<h1>🤖 AI Optimization Complete!</h1><pre>{'<br>'.join(report)}</pre><br><a href='/admin/'>Back to Admin</a>")

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
        sizes = ['S', 'M', 'L', 'XL', 'XXL']
        is_bulk = False
        for size in sizes:
            qty_key = f"bulk_{size}"
            if request.POST.get(qty_key):
                try:
                    qty = int(request.POST.get(qty_key))
                    if qty > 0:
                        is_bulk = True
                        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
                        if not created: cart_item.quantity += qty
                        else: cart_item.quantity = qty
                        cart_item.save()
                except ValueError: continue
        if not is_bulk:
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
    if not created: cart_item.quantity += 1; cart_item.save()
    return redirect('checkout')

def checkout_view(request):
    cart = _get_cart(request)
    if cart.items.count() == 0: return redirect('home')
    total_amount = int(cart.total_price * 100)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount': total_amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, 'store/checkout.html', {'cart': cart, 'cart_count': cart.items.count(), 'razorpay_order_id': payment['id'], 'razorpay_key_id': settings.RAZORPAY_KEY_ID, 'total_price': cart.total_price, 'amount_paise': total_amount})

@csrf_exempt
def order_success_view(request):
    if request.method == "POST":
        cart = _get_cart(request)
        total_qty = sum(item.quantity for item in cart.items.all())
        is_bulk = True if total_qty >= 10 else False
        
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=request.POST.get('full_name', 'Guest'),
            address=request.POST.get('address', 'Online Payment'),
            city=request.POST.get('city', 'India'),
            state=request.POST.get('state', 'TN'),
            country=request.POST.get('country', 'India'),
            zipcode=request.POST.get('zipcode', '000000'),
            phone=request.POST.get('phone', '9999999999'),
            total_amount=cart.total_price, 
            status="Processing", 
            is_bulk_order=is_bulk, 
            qc_passed=False
        )
        
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, price=item.price, quantity=item.quantity)
        
        cart.items.all().delete()

        # 🔥 AUTOMATION TRIGGER
        if order.country.lower() in ['india', 'in']:
            send_order_to_printrove(order)
        else:
            send_order_to_printify(order)

        return render(request, 'store/order_success.html')
    return redirect('home')

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
            country="India", 
            zipcode=request.POST.get('zipcode'),
            phone=request.POST.get('phone'),
            total_amount=cart.total_price,
            status="Processing",
            is_bulk_order=is_bulk,
            qc_passed=False
        )

        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, price=item.price, quantity=item.quantity)

        cart.items.all().delete()
        
        # 🔥 AUTOMATION TRIGGER (COD is mostly India)
        send_order_to_printrove(order)

        return render(request, 'store/order_success.html')
    return redirect('checkout')

# --- DASHBOARDS & OTHER VIEWS ---
@login_required
def upload_design(request):
    if request.method == 'POST':
        form = ProductUploadForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.designer = request.user
            product.is_marketplace = True
            product.cost_price = 300.00
            product.is_approved = True
            product.category = "Community Art"
            product.save()
            return redirect('designer_dashboard')
    else: form = ProductUploadForm()
    return render(request, 'store/upload_design.html', {'form': form})

@login_required
def designer_dashboard(request):
    my_products = Product.objects.filter(designer=request.user)
    sold_items = OrderItem.objects.filter(product__designer=request.user)
    total_earnings = sum((item.product.selling_price - item.product.cost_price) * item.quantity for item in sold_items)
    total_sales_count = sum(item.quantity for item in sold_items)
    return render(request, 'store/designer_dashboard.html', {'products': my_products, 'earnings': total_earnings, 'sales': total_sales_count})

@user_passes_test(lambda u: u.is_superuser)
def owner_dashboard(request):
    today = date.today()
    all_orders = Order.objects.all()
    today_orders = all_orders.filter(created_at__date=today)
    today_revenue = today_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    today_profit = today_orders.aggregate(Sum('net_profit'))['net_profit__sum'] or 0
    
    context = {
        'today_rev': today_revenue,
        'today_orders': today_orders.count(),
        'net_profit': today_profit,
        'pending': all_orders.filter(status='Pending').count(),
        'rto': all_orders.filter(status__in=['Cancelled', 'RTO']).count(),
        'status_counts': all_orders.values('status').annotate(count=Count('id')),
        'top_products': Product.objects.order_by('-sale_count')[:5],
        'bad_products': Product.objects.order_by('-return_count')[:5],
        'country_sales': all_orders.values('country').annotate(total=Sum('total_amount')).order_by('-total'),
        'printrove_count': all_orders.filter(supplier_name="Printrove").count(),
        'printify_count': all_orders.filter(supplier_name="Printify").count(),
    }
    return render(request, 'store/owner_dashboard.html', context)

def custom_design_view(request): return render(request, 'store/custom_design.html')
def save_custom_order(request): return JsonResponse({'status': 'error'}) 

@login_required(login_url='/login/')
def user_profile(request):
    my_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    my_designs = SavedDesign.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/profile.html', {'orders': my_orders, 'designs': my_designs})

@login_required
def reorder_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created: cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@csrf_exempt
@login_required
def save_user_design(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        SavedDesign.objects.create(user=request.user, name=data.get('name'), image_url=data.get('image'))
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

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