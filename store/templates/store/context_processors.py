from .models import Category, SiteSettings

def menu_links(request):
    """Menu bar-la categories kaatta use aagum"""
    categories = Category.objects.prefetch_related('subcategories').all()
    return {
        'categories': categories,
    }

def website_settings(request):
    """Logo matrum site information-kku use aagum"""
    site_config = SiteSettings.objects.first()
    return {
        'site_config': site_config
    }