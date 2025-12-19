from django.contrib import admin
from django.utils.html import format_html
from django.core.files.base import ContentFile
import requests
# 👇 INDHA LINE LA 'SubCategory' ADD PANNIRUKEN (Idhu dhaan fix)
from .models import Category, SubCategory, Product, SiteSettings, HomeBanner
from .utils import get_amazon_details 

# --- ⚡ ACTION: AUTO-FILL FROM AMAZON ---
def fetch_amazon_data(modeladmin, request, queryset):
    count = 0
    for product in queryset:
        if product.affiliate_link and "amazon" in product.affiliate_link:
            try:
                data = get_amazon_details(product.affiliate_link)
                
                if data:
                    product.name = data['name'][:200]
                    if data['price'] > 0:
                        product.selling_price = data['price']
                        product.cost_price = int(data['price'] * 1.4)
                    
                    if data['image_url'] and not product.image:
                        img_resp = requests.get(data['image_url'])
                        if img_resp.status_code == 200:
                            file_name = f"amazon_{product.id}.jpg"
                            product.image.save(file_name, ContentFile(img_resp.content), save=False)
                    
                    product.save()
                    count += 1
            except Exception as e:
                print(f"Skipping {product.id}: {e}")

    modeladmin.message_user(request, f"✅ Successfully Updated {count} Products from Amazon!")
fetch_amazon_data.short_description = "⚡ Auto-Fill Details from Amazon Link"

# --- 1. CATEGORY ADMIN ---
# (Pazhaya CategoryAdmin-a delete pannitu idhai podunga - Inlines use panni SubCategory-a ulla kondu varalam)
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    inlines = [SubCategoryInline] # 👈 Idhu irundha Category kulla ye SubCategory add pannalam!
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius:5px;" />', obj.image.url)
        return "-"

# --- 2. SUB-CATEGORY ADMIN (Thaniya venumna) ---
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

# --- 3. PRODUCT ADMIN ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'selling_price', 'category', 'view_on_amazon')
    list_filter = ('category', 'deal_type')
    search_fields = ('name',)
    list_editable = ('selling_price',)
    actions = [fetch_amazon_data]

    def view_on_amazon(self, obj):
        if obj.affiliate_link:
            return format_html('<a href="{}" target="_blank" style="color:blue;">Link 🔗</a>', obj.affiliate_link)
        return "-"

# --- 4. OTHERS ---
admin.site.register(SiteSettings)
admin.site.register(HomeBanner)