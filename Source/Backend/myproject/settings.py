from pathlib import Path

import os
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#CORS_ALLOW_ALL_ORIGINS = True



# Session konfiguracija (ako je potrebno)
SESSION_COOKIE_SECURE = True  # Postavi na True u produkciji
CSRF_COOKIE_SECURE = True     # Postavi na True u produkciji

CSRF_COOKIE_DOMAIN = ".onrender.com"  # For Render
SESSION_COOKIE_DOMAIN = ".onrender.com"

import mimetypes
mimetypes.add_type("text/css", ".css", True)
BASE_DIR = Path(__file__).resolve().parent.parent

# CSRF TRUSTED ORIGINS (ako koristiš HTTPS u produkciji)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:4200",
    "https://taskmatesbackend-pd5h.onrender.com",
    "https://taskmates-gjhi.onrender.com",
    "https://www.taskmates-gjhi.onrender.com",
    "https://taskmatesbackend-pd5h.onrender.com",
    "https://www.taskmatesbackend-pd5h.onrender.com"
]

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "Authorization",
    "Content-Type",
    "X-CSRFToken",
    "Access-Control-Allow-Origin",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Methods",
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kyd!0nh_+y+u8*g8s(ts7dm2*kbkb@h@#)j(9_wdt+g)&7sprv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '116.203.134.67', #cronjob ip
    '116.203.129.16', #cronjob ip
    '23.88.105.37',   #cronjob ip
    '128.140.8.200',   #cronjob ip
    'taskmatesbackend-pd5h.onrender.com',
    'www.taskmatesbackend-pd5h.onrender.com',
    'angulartaskmates.onrender.com',
    'taskmates-gjhi.onrender.com',
    'www.taskmates-gjhi.onrender.com'
]

CSRF_COOKIE_SAMESITE = None
SESSION_COOKIE_SAMESITE = None

SITE_ID=3
# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'rest_framework',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'core',
    'apps.calendar',
    'apps.groups',
    'apps.notifications',
    'apps.management',
    'apps.tasks',
    'apps.accounts',
    'corsheaders',
    'oauth2_provider',
    'cloudinary', 
    'cloudinary_storage',
    'django_q',
    'apps',
]

Q_CLUSTER = {
    'name': 'DjangoQ2',
    'workers': 4,
    'retry': 60,
    'timeout': 300,
    'save_limit': 250,
    'queue_limit': 500,
    'bulk': 10,
    'orm': 'default',  # Uses Django's ORM
}

SOCIALACCOUNT_LOGIN_ON_GET = True

AUTH_USER_MODEL = 'core.User' ##Bitno za authenticate()

SOCIALACCOUNT_PROVIDERS={
    "google":{
        "SCOPE":[
            "profile","email"
        ],
        "AUTH_PARAMS":{"access_type":"online"}
    }
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
    "accept",
    "origin",
    "x-requested-with"
]

CORS_ALLOW_CREDENTIALS = True  # Omogućuje slanje kolačića s drugih domena

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',  # Prva
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
} 

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY = {
    'CLOUD_NAME': 'djevedi2m',
    'API_KEY': '397716242552879',
    'API_SECRET': 'q1LekeTNsfPraq_u8WdRKdzNGDU',
}
MEDIA_URL = 'https://res.cloudinary.com/djevedi2m/'


ROOT_URLCONF = 'myproject.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse('postgresql://taskmatesbaza_ctl9_user:XabwyUYFAhsWAdtFKgbMjK3kqIiQhdT3@dpg-cu8htn3tq21c73etln30-a.oregon-postgres.render.com/taskmatesbaza_ctl9')
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS=("django.contrib.auth.backends.ModelBackend","allauth.account.auth_backends.AuthenticationBackend")

LOGIN_REDIRECT_URL="https://taskmates-gjhi.onrender.com/my-groups"
LOGOUT_REDIRECT_URL="https://taskmates-gjhi.onrender.com/my-groups"