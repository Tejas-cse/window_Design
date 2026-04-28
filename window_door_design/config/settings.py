import os
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IS_PRODUCTION = os.environ.get('DEBUG', 'True') == 'False'

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-window-door-design-system-2026')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*,localhost,127.0.0.1').split(',')

NEXT_PUBLIC_SUPABASE_URL = os.environ.get('https://yvxtkosszcrakfrrgiun.supabase.co')
NEXT_PUBLIC_SUPABASE_ANON_KEY = os.environ.get('NeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl4dnRrb3NzemNyYWtmcnJnaXVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzcxMjU3MTYsImV4cCI6MjA5MjcwMTcxNn0.GHpg1mg2tC7MJSB355eH0oF4b0fvVXR3DRp6tCD2OBw')

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'design_system',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database configuration - PostgreSQL for production, SQLite for local
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production: Use PostgreSQL from DATABASE_URL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    # Local development: Use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') if not IS_PRODUCTION else '/tmp/staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') if not IS_PRODUCTION else '/tmp/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# PDF and Excel export settings - Use system temp directory for Vercel
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'django_app')
os.makedirs(TEMP_DIR, exist_ok=True)
