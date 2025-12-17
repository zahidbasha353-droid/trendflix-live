from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.views import owner_dashboard  # 👈 Indha Import romba mukkiyam!

urlpatterns = [
    # Custom Dashboard Link (Admin ku mela irukanum)
    path('admin/dashboard/', owner_dashboard, name='owner_dashboard'),
    
    # Default Admin
    path('admin/', admin.site.urls),
    
    # Store App URLs
    path('', include('store.urls')),
]

# Static & Media Files Setup (Image load aaga ithu thevai)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)