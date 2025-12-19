from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, SiteSettings, HomeBanner

# --- 1. CATEGORY ADMIN ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius:5px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image"

# --- 2. PRODUCT ADMIN (Optimized for Affiliate) ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 'deal_type' helps you spot Hot Deals quickly
    # 'view_on_amazon' button allows you to check links directly from admin
    list_display = ('name', 'selling_price', 'category', 'deal_type', 'view_on_amazon')
    list_filter = ('category', 'deal_type')
    search_fields = ('name', 'category__name')
    list_editable = ('selling_price', 'deal_type')

    def view_on_amazon(self, obj):
        if obj.affiliate_link:
            return format_html('<a href="{}" target="_blank" style="background:#FF9900; color:black; padding:5px 10px; border-radius:4px; text-decoration:none; font-weight:bold;">Test Link 🔗</a>', obj.affiliate_link)
        return "No Link"
    view_on_amazon.short_description = "Affiliate Link"

# --- 3. BANNER ADMIN ---
@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ('position', 'main_text', 'image_preview')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius:5px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"

# --- 4. SITE SETTINGS ADMIN ---
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'active_theme')
    
    # Prevents creating multiple settings (One is enough)
    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return True