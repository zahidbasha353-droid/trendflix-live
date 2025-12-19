from .models import Category, SiteSettings

def menu_links(request):
    # Idhu Menu-vukkaana data
    categories = Category.objects.prefetch_related('subcategories').all()
    
    # Idhu Logo & Site Settings kkaana data
    site_config = SiteSettings.objects.first()
    
    return {
        'categories': categories,
        'site_config': site_config
    }