import requests
from bs4 import BeautifulSoup
from django.contrib import admin
from django.utils.html import format_html
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

# --- 3. PRODUCT ADMIN (WITH AUTOMATION BOT) ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Admin List view-la enna theriyanum
    list_display = ('name', 'selling_price', 'category', 'is_approved', 'view_on_amazon')
    list_filter = ('category', 'deal_type', 'is_approved')
    search_fields = ('name',)
    list_editable = ('selling_price', 'is_approved')
    
    # Product Edit page-la enna fields theriyanum
    fields = [
        'amazon_url', 'category', 'name', 'description', 
        'cost_price', 'selling_price', 'affiliate_link', 
        'deal_type', 'is_approved', 'is_trending', 'is_bestseller'
    ]

    def view_on_amazon(self, obj):
        if obj.affiliate_link:
            return format_html('<a href="{}" target="_blank" style="color:blue; font-weight:bold;">Link 🔗</a>', obj.affiliate_link)
        return "-"

    # --- 🤖 THE AUTOMATION BOT LOGIC ---
    def save_model(self, request, obj, form, change):
        # Amazon URL irundhu, Name innum fill aagalana automation start aagum
        if obj.amazon_url and not obj.name:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                    "Accept-Language": "en-US, en;q=0.5"
                }
                response = requests.get(obj.amazon_url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.content, "html.parser")

                # 1. Title/Name Extract pannuvom
                title_tag = soup.find("span", {"id": "productTitle"})
                if title_tag:
                    obj.name = title_tag.get_text().strip()

                # 2. Price Extract (Selling Price)
                price_span = soup.find("span", {"class": "a-price-whole"})
                if price_span:
                    # '1,299' maari irukra string-ah number-ah mathurom
                    price_val = price_span.get_text().replace(',', '').replace('.', '').strip()
                    obj.selling_price = float(price_val)
                    # Automation-kaga cost_price-ah +200 markup vikkirom
                    obj.cost_price = obj.selling_price + 200

                # 3. Image URL Path
                img_tag = soup.find("img", {"id": "landingImage"})
                if img_tag:
                    obj.image_url_path = img_tag.get('src')

                # 4. 🎯 Affiliate Link Generation with zahidbasha-21
                if "tag=" not in obj.amazon_url:
                    separator = "&" if "?" in obj.amazon_url else "?"
                    obj.affiliate_link = f"{obj.amazon_url}{separator}tag=zahidbasha-21"
                else:
                    obj.affiliate_link = obj.amazon_url

            except Exception as e:
                # Oru velai scraping fail aana terminal-la error kaattum
                print(f"Bot Scraping Error: {e}")

        # Final-ah details-ah database-la save pannuvom
        super().save_model(request, obj, form, change)

# --- 4. OTHER MODELS ---
admin.site.register(SiteSettings)
admin.site.register(HomeBanner)