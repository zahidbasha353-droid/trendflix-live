from django.db import models
from django.contrib.auth.models import User

# --- 1. SITE SETTINGS ---
class SiteSettings(models.Model):
    THEME_CHOICES = [
        ('default', 'Default'),
        ('christmas', 'Christmas'),
        ('diwali', 'Diwali'),
        ('sale', 'Big Sale'),
    ]
    site_name = models.CharField(max_length=100, default="TrendFlix")
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    active_theme = models.CharField(max_length=50, choices=THEME_CHOICES, default='default')
    banner = models.ImageField(upload_to='site_banners/', blank=True, null=True)
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.site_name

# --- 2. HOME BANNERS ---
class HomeBanner(models.Model):
    POSITIONS = (
        ('main', 'Main Big Banner (Left Side)'),
        ('side_top', 'Side Top Banner (Right Top)'),
        ('side_bottom', 'Side Bottom Banner (Right Bottom)'),
    )
    
    title = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=20, choices=POSITIONS, unique=True)
    image = models.ImageField(upload_to='banners/')
    small_text = models.CharField(max_length=100, blank=True)
    main_text = models.CharField(max_length=100, blank=True)
    button_text = models.CharField(max_length=50, default="SHOP NOW")
    button_link = models.CharField(max_length=200, default="#")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_position_display()} - {self.title}"

# --- 3. CATEGORY ---
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

# --- 4. SUB-CATEGORY ---
class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} > {self.name}"

# --- 5. PRODUCT (AUTOMATION & AFFILIATE READY) ---
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True) # Automated-ah fill aaga blank=True
    
    # Pudhu field - Amazon URL Input-kaga
    amazon_url = models.URLField(max_length=500, blank=True, null=True, help_text="Amazon product link-ah inga paste pannunga")
    
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    # Scraping images-kaga oru direct URL field (Optional but useful)
    image_url_path = models.URLField(max_length=1000, blank=True, null=True)
    
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    
    affiliate_link = models.URLField(default='https://www.amazon.in/', blank=True, null=True)
    deal_type = models.CharField(max_length=50, choices=[('Hot', 'Hot Deal'), ('New', 'New Arrival'), ('Best', 'Best Seller')], default='New')

    is_approved = models.BooleanField(default=True)
    is_trending = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or "Unnamed Product"

    @property
    def profit(self):
        if self.cost_price > 0:
            discount = ((self.cost_price - self.selling_price) / self.cost_price) * 100
            return int(discount)
        return 0

# --- 6. CART SYSTEM ---
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.selling_price * self.quantity

# --- 7. ORDER SYSTEM ---
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    qc_passed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# --- 8. SAVED DESIGNS ---
class SavedDesign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='designs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)