"""
Django settings for almacen project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5c$9*aa*opbnod$ey4s-53ircc%%&of)8q2t%8==cfawyrtyto'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # para el admin
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'import_export',
    'extra_settings',
    'qr_code',
    'widget_tweaks',
    'pwa',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'prestamos'
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

ROOT_URLCONF = 'almacen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'almacen.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'almacen',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '3306',
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

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Tijuana'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / STATIC_URL

# Archivos subidos desde django
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / MEDIA_URL #'/media/'
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login
LOGIN_REDIRECT_URL = 'order_list'
LOGOUT_REDIRECT_URL = '/'

# admin personalizado
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# extra settings
# settings.py

EXTRA_SETTINGS_DEFAULTS = [
    {
        "name": "STORE_OPENING_TIME",
        "type": "time",
        "value": "09:00",
        "description": "Store opening time",
        "editable": True,
    },
    {
        "name": "STORE_CLOSING_TIME",
        "type": "time",
        "value": "18:00",
        "description": "Store closing time",
        "editable": True,
    },
    {
        "name": "STORE_OPEN_DAYS",
        "type": "string",
        "value": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday",
        "description": "Days of the week the store is open, separated by commas",
        "editable": True,
    },
    {
        "name": "BLOCK_REQUESTS_IF_REPORTS",
        "type": "bool",
        "value": False,
        "description": "Block new requests if the account has active reports",
        "editable": True,
    },
    # Información de contacto del almacén
    {
        "name": "WAREHOUSE_PHONE",
        "type": "string",
        "value": "+00 0000000000",
        "description": "Warehouse contact phone number",
        "editable": True,
    },
    {
        "name": "WAREHOUSE_EMAIL",
        "type": "string",
        "value": "warehouse@doe.com",
        "description": "Warehouse contact email",
        "editable": True,
    },
    # Información de contacto del soporte
    {
        "name": "SUPPORT_PHONE",
        "type": "string",
        "value": "+00 0000000000",
        "description": "Support contact phone number",
        "editable": True,
    },
    {
        "name": "SUPPORT_EMAIL",
        "type": "string",
        "value": "joe@doe.com",
        "description": "Support contact email",
        "editable": True,
    },
    {
        "name": "CATALOG_ITEMS_PAGINATION",
        "type": "int",
        "value": 20,
        "description": "Elementos en una pagina del catalogo",
        "editable": True,
    }
]

# PWA
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = LANGUAGE_CODE
PWA_APP_NAME = 'Prueba de Prestamos'
PWA_APP_DESCRIPTION = "Prueba de prestamos"
PWA_APP_THEME_COLOR = '#000000'
PWA_APP_BACKGROUND_COLOR = '#000000'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': 'static/img.jpg',
        'sizes': '160x160'
    }
]

PWA_APP_ICONS_APPLE = [
    {
        'src': 'static/img.jpg',
        'sizes': '160x160'
    }
]

PWA_APP_SPLASH_SCREEN = [
    {
        'src': 'static/img.jpg',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]

PWA_APP_SCREENSHOTS = [
    {
        'src': 'static/screenshot/1.png',
        'sizes': '750x1334',
        "type": "image/png"
    },
    {
        'src': 'static/screenshot/2.png',
        'sizes': '750x1334',
        "type": "image/png"
    },
    {
        'src': 'static/screenshot/3.png',
        'sizes': '750x1334',
        "type": "image/png"
    },
    {
        'src': 'static/screenshot/4.png',
        'sizes': '750x1334',
        "type": "image/png"
    },
    {
        'src': 'static/screenshot/5.png',
        'sizes': '750x1334',
        "type": "image/png"
    },
    {
        'src': 'static/screenshot/6.png',
        'sizes': '750x1334',
        "type": "image/png"
    },
    {
        'src': 'static/screenshot/7.png',
        'sizes': '750x1334',
        "type": "image/png"
    },
]
