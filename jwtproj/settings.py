import os  # <-- ADD THIS IMPORT for environment variables
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# 1. Load SECRET_KEY from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-ehdk8%d@(%r%77kosleoodfd=oegrqn6gp9(wnfh36_y-b!+n-')

# SECURITY WARNING: don't run with debug turned on in production!
# 2. Set DEBUG based on environment variable (False in production)
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# 3. Allow Wasmer Edge hosts
ALLOWED_HOSTS = [
    '.wasmer.app',         # Allow Wasmer Edge domains
    os.environ.get('WASMER_APP_HOSTNAME'), # Allow the specific hostname
    # '127.0.0.1',           # Keep for local testing
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
            ],
        },
    },
]

WSGI_APPLICATION = 'jwtproj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.environ.get('DB_NAME', 'jwt'),
#         'USER': os.environ.get('DB_USER', 'root'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'As@8675db'),
#         # Host/Port MUST be changed to your *production* database's address on Wasmer
#         # For a separate database service, this would be its internal or external address
#         'HOST': os.environ.get('DB_HOST', 'localhost'), 
#         'PORT': os.environ.get('DB_PORT', '3306'),
#     }
# }

# DATABASES for initial Wasmer deploy (using SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', # This file will be created inside your volume
    }
}



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

# 5. Static Files Configuration (Necessary for collectstatic, even if not served by Django)
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
