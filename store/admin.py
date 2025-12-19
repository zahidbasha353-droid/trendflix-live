from django.contrib import admin
from django.utils.html import format_html
from .models import Category, SubCategory, Product, SiteSettings, HomeBanner

# --- 1. CATEGORY ADMIN ---
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

# --- 3. PRODUCT ADMIN ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'selling_price', 'category', 'view_on_amazon')
    list_filter = ('category', 'deal_type')
    search_fields = ('name',)
    list_editable = ('selling_price',)
    
    # Actions line-a remove panniten due to error
    # actions = [fetch_amazon_data] 

    def view_on_amazon(self, obj):
        if obj.affiliate_link:
            return format_html('<a href="{}" target="_blank" style="color:blue;">Link 🔗</a>', obj.affiliate_link)
        return "-"

# --- 4. OTHERS ---
admin.site.register(SiteSettings)
admin.site.register(HomeBanner)