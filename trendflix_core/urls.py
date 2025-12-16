from django.contrib import admin
from django.urls import path, include  # <-- Inga 'include' irukkanum

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),   # <-- Ithu mukkiyam
]