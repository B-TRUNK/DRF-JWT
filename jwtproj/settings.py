import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ==== SECURITY (Wasmer injects these) ====
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "O_2eY7mg2JOflMK1JFKvAxYhxtk8v6Q0_eRePgO7psErA6tnCPj6KEKNbqbgeNxrglc"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,wasmer.app").split(",")

# ==== DATABASE (Wasmer auto-provisions) ====
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DJANGO_DB_NAME", "jwt"),
        "USER": os.environ.get("DJANGO_DB_USER", "root"),
        "PASSWORD": os.environ.get("DJANGO_DB_PASSWORD", ""),
        "HOST": os.environ.get("DJANGO_DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DJANGO_DB_PORT", "3306"),
    }
}

# ==== STATIC FILES ====
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==== REST FRAMEWORK & JWT ====
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}