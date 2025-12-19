import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-change-me-later-to-something-secure'
DEBUG = True
ALLOWED_HOSTS = ['zahidbasha.pythonanywhere.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'jazzmin',  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store', 
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trendflix_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.website_settings',
                'store.context_processors.menu_links',
            ],
        },
    },
]

WSGI_APPLICATION = 'trendflix_core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Merge panna Jazzmin Settings
JAZZMIN_SETTINGS = {
    "site_title": "TrendFlix HQ",
    "site_header": "TrendFlix",
    "site_brand": "TrendFlix Owner",
    "welcome_sign": "Welcome back, Boss!",
    "copyright": "TrendFlix Ltd",
    "search_model": "store.Product",
    "custom_links": {
        "store": [{
            "name": "Owner Dashboard", 
            "url": "owner_dashboard", 
            "icon": "fas fa-crown",
        }]
    },
    "order_with_respect_to": ["store", "auth", "orders"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "store.Product": "fas fa-tshirt",
        "store.Order": "fas fa-shopping-cart",
    },
}

RAZORPAY_KEY_ID = 'rzp_live_Rrq5jqy3nk3pA6'
RAZORPAY_KEY_SECRET = 'waywumrUF8mLOG0JuUKb9hDF'