"""
Django settings for the Luke The Plumber project.

A professional website for a UK (England) based plumbing company,
including customer accounts (register / login / logout) and a
quote-request system.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------
# SECURITY
# -----------------------------------------------------------------------
# NOTE: Keep this secret in production. For local development this is fine,
# but before deploying, move it to an environment variable.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-CHANGE-THIS-KEY-BEFORE-DEPLOYING-luke-plumber-2026'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Render sets RENDER_EXTERNAL_HOSTNAME automatically — pick it up so you
# don't have to set DJANGO_ALLOWED_HOSTS by hand.
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# PythonAnywhere hostnames end in .pythonanywhere.com — allow them by default
# so the site works before you've set DJANGO_ALLOWED_HOSTS.
ALLOWED_HOSTS.append('.pythonanywhere.com')

CSRF_TRUSTED_ORIGINS = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',') \
    if os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS') else []
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# -----------------------------------------------------------------------
# APPLICATION DEFINITION
# -----------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'core',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'luke_plumber.urls'

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
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'luke_plumber.wsgi.application'
ASGI_APPLICATION = 'luke_plumber.asgi.application'

# -----------------------------------------------------------------------
# DATABASE
# -----------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------------------------------------------------
# PASSWORD VALIDATION
# -----------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------------------------------------------------
# INTERNATIONALIZATION -- configured for England / UK
# -----------------------------------------------------------------------
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------
# STATIC & MEDIA FILES
# -----------------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise serves static files directly from Django/Gunicorn in production
# (used on Render). Compresses files and adds cache-busting hashed filenames.
# Falls back to plain storage when DEBUG=True so runserver keeps working.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        if not DEBUG else "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------------------
# AUTHENTICATION
# -----------------------------------------------------------------------
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:profile'
LOGOUT_REDIRECT_URL = 'core:home'

# -----------------------------------------------------------------------
# EMAIL (console backend for development -- swap for SMTP in production)
# -----------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'Luke The Plumber <no-reply@luketheplumber.co.uk>'

# -----------------------------------------------------------------------
# SITE / BUSINESS DETAILS (used across templates via context processor)
# -----------------------------------------------------------------------
SITE_NAME = 'Luke The Plumber'
SITE_PHONE = '020 7946 0958'
SITE_EMERGENCY_PHONE = '07700 900 123'
SITE_EMAIL = 'info@luketheplumber.co.uk'
SITE_ADDRESS = '14 Victoria Street, Westminster, London, SW1H 0NB'
SITE_GAS_SAFE_NUMBER = '123456'

# Full base URL of the deployed site (no trailing slash), used to build
# links inside WhatsApp notification messages, e.g.
# "https://luke-the-plumber.onrender.com"
SITE_URL = os.environ.get('SITE_URL', 'http://127.0.0.1:8000')

# -----------------------------------------------------------------------
# WHATSAPP NOTIFICATIONS (via Twilio)
# -----------------------------------------------------------------------
# Sends a WhatsApp message to the business owner whenever a customer
# submits the contact/quote form. Requires a (free to start) Twilio
# account with the WhatsApp Sandbox — or a production WhatsApp Business
# sender once approved. Leave the SID/token blank to disable notifications
# without breaking the site — the form will still work and save to the
# database either way.
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
# Twilio's shared WhatsApp Sandbox number — replace once you have your own
# approved WhatsApp Business sender number.
TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
# The business owner's WhatsApp number that receives new-enquiry alerts.
ADMIN_WHATSAPP_NUMBER = os.environ.get('ADMIN_WHATSAPP_NUMBER', 'whatsapp:+2347068848255')
