from .models import Category, SiteSettings

def menu_links(request):
    # Idhu Menu categories-kkaana data
    try:
        categories = Category.objects.prefetch_related('subcategories').all()
    except:
        categories = None
    
    return {
        'categories': categories,
    }

def website_settings(request):
    # Idhu Logo & Site Settings-kkaana data
    try:
        site_config = SiteSettings.objects.first()
    except:
        site_config = None
        
    return {
        'site_config': site_config
    }