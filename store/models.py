from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 1. CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    def __str__(self): return self.name

# 2. PRODUCT
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default="T-Shirt") 
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    designer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_marketplace = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=300.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    printrove_variant_id = models.CharField(max_length=50, blank=True, null=True, help_text="India Variant ID (Printrove)") 
    printify_product_id = models.CharField(max_length=100, blank=True, null=True, help_text="Global Product ID (Printify)")
    printify_variant_id = models.CharField(max_length=100, blank=True, null=True, help_text="Global Variant ID (Printify)")

    is_ai_generated = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    sale_count = models.IntegerField(default=0)
    return_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def profit_margin(self):
        return self.selling_price - self.cost_price

    def __str__(self): return self.name

# 3. CART
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, default="M")

    @property
    def price(self):
        if self.quantity >= 10: return int(self.product.selling_price * 0.90)
        return self.product.selling_price

    @property
    def total_price(self):
        return self.price * self.quantity

# 4. ORDER (Tracking Number Added Here)
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'), ('Processing', 'Processing'),
        ('Shipped', 'Shipped'), ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'), ('RTO', 'RTO (Returned)')
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    zipcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    print_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    tracking_number = models.CharField(max_length=100, blank=True, null=True) # ✅ Added!
    supplier_name = models.CharField(max_length=50, default="Pending", blank=True)
    supplier_order_id = models.CharField(max_length=100, blank=True, null=True)
    api_response = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_bulk_order = models.BooleanField(default=False)
    qc_passed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.net_profit = self.total_amount - (self.print_cost + self.shipping_cost)
        super(Order, self).save(*args, **kwargs)

    def __str__(self): return f"Order #{self.id}"

# 5. ORDER ITEM (இதுதான் மிஸ் ஆச்சு - இப்போ சேர்த்தாச்சு)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self): return f"{self.quantity} x {self.product.name}"

# 6. SAVED DESIGN
class SavedDesign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="My Custom Design")
    image_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): return f"{self.user.username} - {self.name}"