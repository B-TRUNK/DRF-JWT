# jwtproj/settings.py
import os
import sys
from pathlib import Path
from datetime import timedelta

import dj_database_url
import pymysql
from dotenv import load_dotenv

# -------------------------------------------------
# 1. PyMySQL → replace MySQLdb (required for Wasmer)
# -------------------------------------------------
pymysql.install_as_MySQLdb()

# -------------------------------------------------
# 2. Load .env (local dev only)
# -------------------------------------------------
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# -------------------------------------------------
# 3. Base directory
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------
# 4. Security & Debug
# -------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-local-secret-change-me")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

# -------------------------------------------------
# 5. Allowed hosts (Wasmer + local)
# -------------------------------------------------
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost,.wasmer.app").split(",")
    if h.strip()
]

# -------------------------------------------------
# 6. DATABASE CONFIG — PRIORITY: DATABASE_URL
# -------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")

print(f"DATABASE_URL = {DATABASE_URL}", file=sys.stderr)  # Debug log

if DATABASE_URL:
    # Use dj_database_url to parse full URL (recommended)
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True if "sslmode=require" in DATABASE_URL else False,
        )
    }
    print("Database configured via DATABASE_URL", file=sys.stderr)
else:
    # Fallback: SQLite (safe for local dev or missing config)
    print("WARNING: DATABASE_URL not set → using SQLite fallback", file=sys.stderr)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Optional: Print redacted DB config in DEBUG mode
if DEBUG:
    import logging
    log = logging.getLogger("django")
    db_copy = DATABASES["default"].copy()
    if "PASSWORD" in db_copy:
        db_copy["PASSWORD"] = "***REDACTED***"
    log.warning("DATABASES config (redacted): %s", db_copy)

# -------------------------------------------------
# 7. Apps
# -------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
    "rest_framework",
    "rest_framework_simplejwt",
    "djoser",
]

# -------------------------------------------------
# 8. REST Framework + JWT
# -------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# -------------------------------------------------
# 9. Middleware
# -------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------------------------------
# 10. URLs & Templates
# -------------------------------------------------
ROOT_URLCONF = "jwtproj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "jwtproj.wsgi.application"

# -------------------------------------------------
# 11. Password validation
# -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------------------------
# 12. Internationalization
# -------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# 13. Static files (Whitenoise)
# -------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -------------------------------------------------
# 14. Default primary key
# -------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------
# 15. Production security headers
# -------------------------------------------------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 60 * 60 * 24 * 7))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True") == "True"
    SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "False") == "True"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Trust Wasmer domains
    CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if h and not h.startswith(".")]

# -------------------------------------------------
# 16. Logging (console only)
# -------------------------------------------------
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}

# -------------------------------------------------
# 17. JWT Settings (optional, customize as needed)
# -------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
}