from django.db import models
from django.contrib.auth.models import User

# --- CATEGORY MODEL (For Dynamic Homepage) ---
class Category(models.Model):
    name = models.CharField(max_length=100)  # Category peyar (e.g., Men, Women)
    image = models.ImageField(upload_to='category_images/') # Category image
    
    def __str__(self):
        return self.name

# --- PRODUCT MODEL ---
class Product(models.Model):
    # MARKETPLACE FIELDS
    designer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_marketplace = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)

    # BASIC FIELDS
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=300.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    category = models.CharField(max_length=100, default="T-Shirt") # Note: Ithu text field. Future la Category model ku link pannalam.
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 🔥 AI BRAIN FIELDS
    view_count = models.PositiveIntegerField(default=0)
    is_bestseller = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    ai_pricing_active = models.BooleanField(default=True)

    @property
    def profit(self):
        return self.selling_price - self.cost_price

    def __str__(self):
        tag = "🔥 " if self.is_trending else ""
        return f"{tag}{self.name}"

# --- CART SYSTEM ---
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

# --- ORDER SYSTEM ---
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
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    zipcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    is_bulk_order = models.BooleanField(default=False)
    qc_passed = models.BooleanField(default=False)

    supplier_name = models.CharField(max_length=50, default="Pending", blank=True)
    supplier_order_id = models.CharField(max_length=100, blank=True, null=True)
    api_response = models.TextField(blank=True, null=True)

    def __str__(self): return f"Order #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self): return f"{self.quantity} x {self.product.name}"

class SavedDesign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="My Custom Design")
    image_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): return f"{self.user.username} - {self.name}"

# --- SITE SETTINGS (Dynamic Admin Control) ---
class SiteSettings(models.Model):
    THEME_CHOICES = [
        ('default', 'Default (No Effect)'),
        ('christmas', '❄️ Christmas / New Year (Snow)'),
        ('diwali', '🪔 Diwali / Eid (Golden Lights)'),
        ('sale', '🎉 Big Sale (Confetti)'),
    ]

    site_name = models.CharField(max_length=100, default="TrendFlix")
    
    # Neenga ketta "New Code" Fields:
    banner = models.ImageField(upload_to='site_banners/', blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    
    # Extra fields for full control
    logo = models.ImageField(upload_to='site_assets/', help_text="Upload transparent PNG logo", blank=True, null=True)
    active_theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='default')
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
        # Corrected: Removed the 'models =' line that caused the error

    def __str__(self):
        return "Website Configuration"
    # --- BANNER MODEL ---
class HomeBanner(models.Model):
    POSITIONS = (
        ('main', 'Main Big Banner (Left Side)'),
        ('side_top', 'Side Top Banner (Right Top)'),
        ('side_bottom', 'Side Bottom Banner (Right Bottom)'),
    )
    
    position = models.CharField(max_length=20, choices=POSITIONS, unique=True, help_text="Select where this banner should appear")
    image = models.ImageField(upload_to='banners/')
    
    # Text Control
    small_text = models.CharField(max_length=100, help_text="Ex: New Collection (Top small text)")
    main_text = models.CharField(max_length=100, help_text="Ex: Summer Sale (Big bold text)")
    
    # Button Control
    button_text = models.CharField(max_length=50, default="SHOP NOW")
    button_link = models.CharField(max_length=200, default="#", help_text="Paste product or category link here")
    
    def __str__(self):
        return self.get_position_display()