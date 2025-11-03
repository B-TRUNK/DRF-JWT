# jwtproj/settings.py
import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Load .env in local development if present
# On Wasmer you will set env vars via app.yaml so this simply is a no-op there.
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# BASE_DIR: project root (DRF-JWT/)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY: read from environment or use a development fallback (don't use fallback in production)
SECRET_KEY = os.environ.get('SECRET_KEY', 'unsafe-local-secret-change-me')

# DEBUG: boolean. Set DEBUG=False in production env.
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('1', 'true', 'yes')

# ALLOWED_HOSTS: comma-separated list in env var, default includes local and Wasmer wildcard
ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get('ALLOWED_HOSTS', '127.0.0.1,.wasmer.app').split(',')
    if h.strip()
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog',
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
]


REST_FRAMEWORK = {


    # simple jwt auth from documentation
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication', #API based authentication
        'rest_framework.authentication.SessionAuthentication',       #Browser based authentication   
    ),

    # permissions
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    

}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise for serving static files in production without needing nginx
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jwtproj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jwtproj.wsgi.application'


# --- DATABASE CONFIG ---

import sys
print("DATABASE_URL =", os.environ.get("DATABASE_URL"), file=sys.stderr)

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600),
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DATABASE_ENGINE", "django.db.backends.mysql"),
            "NAME": os.environ.get("DATABASE_NAME"),
            "USER": os.environ.get("DATABASE_USER"),
            "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
            "HOST": os.environ.get("DATABASE_HOST", "127.0.0.1"),
            "PORT": os.environ.get("DATABASE_PORT", "3306"),
        },
    }


# Helpful debugging: show what Django sees when DEBUG is enabled
if os.environ.get('DEBUG', 'False').lower() in ('1', 'true', 'yes'):
    # Print a redacted version of DATABASES to console so you can verify values locally.
    import logging
    log = logging.getLogger('django')
    db_dbg = DATABASES.get('default', {}).copy()
    if 'PASSWORD' in db_dbg:
        db_dbg['PASSWORD'] = '***REDACTED***'
    log.warning("DATABASES config (redacted): %s", db_dbg)


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # where collectstatic will gather files

# Whitenoise: compress and cache static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========== Security toggles for production ==========
if not DEBUG:
    # Recommended headers when using a reverse proxy / edge provider
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Strict transport security — if you have HTTPS handled by Wasmer you can enable these
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 60 * 60 * 24 * 7))  # default 1 week
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
    SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'False') == 'True'

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Trust the Wasmer domains or your custom domain(s)
    CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if h and not h.startswith('.')]


# ========== Logging (simple console logger) ==========
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{'class': 'logging.StreamHandler',},
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
}

