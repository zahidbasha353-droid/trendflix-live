import requests
from bs4 import BeautifulSoup
from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, SubCategory, Product, SiteSettings, HomeBanner

# --- 1. CATEGORY ADMIN (With Inlines) ---
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    inlines = [SubCategoryInline]
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius:5px;" />', obj.image.url)
        return "-"

# --- 2. SUB-CATEGORY ADMIN ---
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

# --- 3. PRODUCT ADMIN (WITH BOT & AUTO-UPDATE LOGIC) ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Admin List view-la fields
    list_display = ('name', 'selling_price', 'category', 'deal_type', 'is_approved', 'view_on_amazon')
    list_filter = ('category', 'deal_type', 'is_approved', 'is_trending')
    search_fields = ('name',)
    list_editable = ('selling_price', 'is_approved', 'deal_type')
    
    fields = [
        'amazon_url', 'category', 'name', 'description', 
        'cost_price', 'selling_price', 'affiliate_link', 
        'deal_type', 'is_approved', 'is_trending', 'is_bestseller'
    ]

    def view_on_amazon(self, obj):
        if obj.affiliate_link:
            return format_html('<a href="{}" target="_blank" style="color:#FF9900; font-weight:bold;">Amazon 🔗</a>', obj.affiliate_link)
        return "-"

    # --- 🚀 Pudhu Logic: Single Click Update Context ---
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Template-la buttons kaatta intha variable useful-ah irukkum
        extra_context['update_buttons'] = True
        return super().changelist_view(request, extra_context=extra_context)

    # --- 🤖 Old Logic: Automatic Scraping (Manual URL Paste panna) ---
    def save_model(self, request, obj, form, change):
        if obj.amazon_url and not obj.name:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                    "Accept-Language": "en-US, en;q=0.5"
                }
                response = requests.get(obj.amazon_url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.content, "html.parser")

                # 1. Title
                title_tag = soup.find("span", {"id": "productTitle"})
                if title_tag:
                    obj.name = title_tag.get_text().strip()

                # 2. Price & Auto-Markup
                price_span = soup.find("span", {"class": "a-price-whole"})
                if price_span:
                    price_val = price_span.get_text().replace(',', '').replace('.', '').strip()
                    obj.selling_price = float(price_val)
                    obj.cost_price = obj.selling_price + 200 # Profit margin

                # 3. Image URL
                img_tag = soup.find("img", {"id": "landingImage"})
                if img_tag:
                    obj.image_url_path = img_tag.get('src')

                # 4. Affiliate Tagging (zahidbasha-21)
                if "tag=" not in obj.amazon_url:
                    separator = "&" if "?" in obj.amazon_url else "?"
                    obj.affiliate_link = f"{obj.amazon_url}{separator}tag=zahidbasha-21"
                else:
                    obj.affiliate_link = obj.amazon_url

                messages.success(request, f"Bot successfully scraped: {obj.name[:50]}...")
            except Exception as e:
                messages.error(request, f"Bot Scraping Error: {e}")

        super().save_model(request, obj, form, change)

# --- 4. OTHER MODELS ---
admin.site.register(SiteSettings)
admin.site.register(HomeBanner)