"""
Django settings for trendflix project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-change-me-later-to-something-secure'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 🔥 முக்கியம்: இது இருந்தா தான் PythonAnywhere-ல் வேலை செய்யும்
ALLOWED_HOSTS = ['zahidbasha.pythonanywhere.com', 'localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'jazzmin',  # 🔥 Admin டிசைனுக்காக (இது மேலே இருக்கணும்)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # நம்முடைய Apps & Libraries
    'store',            # நம்ம கடை
    'rest_framework',   # API-க்காக
    # 'razorpay',       # பேமெண்ட் (தேவைப்பட்டால் இதை uncomment பண்ணலாம்)
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

ROOT_URLCONF = 'trendflix_core.urls'  # குறிப்பு: உங்க மெயின் ஃபோல்டர் பெயர் வேறனா இதை மாத்தணும்

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
                
                # Namma puthusa add panna line
                'store.context_processors.website_settings',
                'store.context_processors.menu_links',
            ],
        },
    },
]
WSGI_APPLICATION = 'trendflix_core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# 🔥 முக்கியம்: சர்வரில் டிசைன் வர இது கண்டிப்பா இருக்கணும்
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media Files (Product Images upload பண்ண)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Jazzmin Settings (Admin டிசைன்)
JAZZMIN_SETTINGS = {
    "site_title": "TrendFlix Admin",
    "site_header": "TrendFlix",
    "welcome_sign": "Welcome to TrendFlix HQ",
    "search_model": "store.Product",
    "user_avatar": None,
}
# RAZORPAY SETTINGS
RAZORPAY_KEY_ID = 'rzp_live_Rrq5jqy3nk3pA6'  # Unga Key ID inga podunga
RAZORPAY_KEY_SECRET = 'waywumrUF8mLOG0JuUKb9hDF'   # Unga Secret Key inga podunga
# JAZZMIN SETTINGS (Admin Sidebar Customization)
JAZZMIN_SETTINGS = {
    "site_title": "TrendFlix HQ",
    "site_header": "TrendFlix",
    "site_brand": "TrendFlix Owner",
    "welcome_sign": "Welcome back, Boss!",
    "copyright": "TrendFlix Ltd",
    
    # Custom Links (Ithu dhaan mukkiyam)
    "custom_links": {
        "store": [{
            "name": "Owner Dashboard", 
            "url": "owner_dashboard", 
            "icon": "fas fa-crown",
        }]
    },
    
    # Order of apps in sidebar
    "order_with_respect_to": ["store", "auth", "orders"],
    
    # Icons for models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "store.Product": "fas fa-tshirt",
        "store.Order": "fas fa-shopping-cart",
    },
}