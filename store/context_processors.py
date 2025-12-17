from .models import SiteSettings

def website_settings(request):
    # Get the last added setting, or return None
    settings = SiteSettings.objects.last()
    return {'site_config': settings}