from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# 1. CATEGORY (New Code Style - Better)
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

# 2. PRODUCT (Merged: Old Features + New Fixes)
class Product(models.Model):
    # Basic Info
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    
    # Pricing (Changed 'selling_price' to 'price' to fix errors)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=300.00)
    
    # Images
    image = models.ImageField(upload_to='images/')
    image_url = models.URLField(max_length=500, blank=True, null=True) # Script needs this
    
    # Status
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Print-on-Demand Fields (From Old Code)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.name

# 3. CART (From Old Code)
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
    def total_price(self):
        return self.product.price * self.quantity

# 4. ORDER (From Old Code)
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Order #{self.id}"

# 5. ORDER ITEM (From Old Code)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self): return f"{self.quantity} x {self.product.name}"

# 6. SAVED DESIGN (For 3D Lab)
class SavedDesign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="My Custom Design")
    image_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): return f"{self.user.username} - {self.name}"