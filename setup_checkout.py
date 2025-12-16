import os

# PATHS
base_dir = os.getcwd()
store_dir = os.path.join(base_dir, 'store')
templates_dir = os.path.join(store_dir, 'templates', 'store')

# ---------------------------------------------------------
# 1. UPDATE MODELS (Adding Advanced Order System)
# ---------------------------------------------------------
models_code = """from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=500)
    sku = models.CharField(max_length=50, unique=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    reviews_count = models.IntegerField(default=100)
    is_bestseller = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.selling_price * self.quantity

# New Order Models
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
"""
with open(os.path.join(store_dir, 'models.py'), 'w', encoding='utf-8') as f:
    f.write(models_code)
print("✅ Models Updated (Order System Ready)")

# ---------------------------------------------------------
# 2. UPDATE URLS (Adding Checkout Links)
# ---------------------------------------------------------
urls_code = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/', views.order_success_view, name='order_success'),
]
"""
with open(os.path.join(store_dir, 'urls.py'), 'w', encoding='utf-8') as f:
    f.write(urls_code)
print("✅ URLs Updated (Checkout Added)")

# ---------------------------------------------------------
# 3. UPDATE VIEWS (Checkout Logic)
# ---------------------------------------------------------
views_code = """from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Cart, CartItem, Order, OrderItem

def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def home(request):
    products = Product.objects.all()
    cart = _get_cart(request)
    return render(request, 'store/home.html', {'products': products, 'cart_count': cart.items.count()})

def cart_view(request):
    cart = _get_cart(request)
    return render(request, 'store/cart.html', {'cart': cart, 'cart_count': cart.items.count()})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')

def checkout_view(request):
    cart = _get_cart(request)
    if cart.items.count() == 0:
        return redirect('home')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        phone = request.POST.get('phone')

        # Create Order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            phone=phone,
            total_amount=cart.total_price
        )

        # Move Items from Cart to Order
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.quantity
            )
        
        # Clear Cart
        cart.items.all().delete()
        
        return redirect('order_success')

    return render(request, 'store/checkout.html', {'cart': cart, 'cart_count': cart.items.count()})

def order_success_view(request):
    return render(request, 'store/order_success.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
"""
with open(os.path.join(store_dir, 'views.py'), 'w', encoding='utf-8') as f:
    f.write(views_code)
print("✅ Views Updated (Checkout Logic Added)")

# ---------------------------------------------------------
# 4. CREATE CHECKOUT HTML
# ---------------------------------------------------------
checkout_html = """{% extends 'store/base.html' %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <h3 class="mb-4">Checkout</h3>
        <div class="card p-4 shadow-sm">
            <form method="POST">
                {% csrf_token %}
                <h5 class="mb-3">Shipping Details</h5>
                <div class="mb-3">
                    <label>Full Name</label>
                    <input type="text" name="full_name" class="form-control" required placeholder="John Doe">
                </div>
                <div class="mb-3">
                    <label>Address</label>
                    <textarea name="address" class="form-control" rows="2" required placeholder="123 Street Name"></textarea>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label>City</label>
                        <input type="text" name="city" class="form-control" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label>State</label>
                        <input type="text" name="state" class="form-control" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label>Zip Code</label>
                        <input type="text" name="zipcode" class="form-control" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label>Phone Number</label>
                        <input type="text" name="phone" class="form-control" required>
                    </div>
                </div>
                
                <h5 class="mb-3 mt-4">Payment Method</h5>
                <div class="form-check mb-3">
                    <input class="form-check-input" type="radio" name="payment" checked>
                    <label class="form-check-label">Cash on Delivery (COD)</label>
                </div>
                <div class="form-check mb-3">
                    <input class="form-check-input" type="radio" name="payment" disabled>
                    <label class="form-check-label text-muted">Credit Card (Coming Soon)</label>
                </div>

                <button type="submit" class="btn btn-warning w-100 btn-lg mt-3">Place Order</button>
            </form>
        </div>
    </div>
    
    <div class="col-md-4">
        <h4 class="mb-4">Order Summary</h4>
        <div class="card p-3 shadow-sm bg-light">
            <ul class="list-group list-group-flush mb-3">
                {% for item in cart.items.all %}
                <li class="list-group-item d-flex justify-content-between lh-sm bg-light">
                    <div>
                        <h6 class="my-0">{{ item.product.name }}</h6>
                        <small class="text-muted">Qty: {{ item.quantity }}</small>
                    </div>
                    <span class="text-muted">₹{{ item.total_price }}</span>
                </li>
                {% endfor %}
                <li class="list-group-item d-flex justify-content-between bg-light fw-bold">
                    <span>Total (INR)</span>
                    <span>₹{{ cart.total_price }}</span>
                </li>
            </ul>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(templates_dir, 'checkout.html'), 'w', encoding='utf-8') as f:
    f.write(checkout_html)
print("✅ Checkout Page Created")

# ---------------------------------------------------------
# 5. CREATE SUCCESS HTML
# ---------------------------------------------------------
success_html = """{% extends 'store/base.html' %}
{% block content %}
<div class="text-center mt-5">
    <div class="mb-4">
        <i class="fa-solid fa-circle-check text-success" style="font-size: 80px;"></i>
    </div>
    <h1 class="mb-3">Thank You for Your Order!</h1>
    <p class="lead text-muted">Your order has been placed successfully.</p>
    <p>We will contact you shortly for delivery.</p>
    <a href="{% url 'home' %}" class="btn btn-primary mt-3">Continue Shopping</a>
</div>
{% endblock %}
"""
with open(os.path.join(templates_dir, 'order_success.html'), 'w', encoding='utf-8') as f:
    f.write(success_html)
print("✅ Order Success Page Created")

# ---------------------------------------------------------
# 6. UPDATE CART HTML (Link Button to Checkout)
# ---------------------------------------------------------
cart_html = """{% extends 'store/base.html' %}
{% block content %}
<div class="container">
    <h2 class="mb-4">Shopping Cart</h2>
    {% if cart.items.all %}
    <div class="card p-3 shadow-sm">
        <table class="table">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Total</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for item in cart.items.all %}
                <tr>
                    <td>
                        <img src="{{ item.product.image_url }}" style="height: 50px; width: 50px; object-fit: contain;">
                        {{ item.product.name }}
                    </td>
                    <td>₹{{ item.product.selling_price }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>₹{{ item.total_price }}</td>
                    <td>
                        <a href="{% url 'remove_from_cart' item.id %}" class="btn btn-sm btn-danger"><i class="fa-solid fa-trash"></i></a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <div class="text-end mt-3">
            <h4>Subtotal: ₹{{ cart.total_price }}</h4>
            <a href="{% url 'checkout' %}" class="btn btn-warning btn-lg mt-2">Proceed to Checkout</a>
        </div>
    </div>
    {% else %}
    <div class="alert alert-info">Your cart is empty. <a href="{% url 'home' %}">Continue Shopping</a></div>
    {% endif %}
</div>
{% endblock %}
"""
with open(os.path.join(templates_dir, 'cart.html'), 'w', encoding='utf-8') as f:
    f.write(cart_html)
print("✅ Cart Page Updated (Link Active)")

print("-" * 30)
print("🚀 CHECKOUT SYSTEM READY!")
print("Run migrations now!")
print("-" * 30)