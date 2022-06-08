import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DATABASE_NAME", "accounts"),
        "USER": os.environ.get("DATABASE_USER", "postgres"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "secret"),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DATABASE_PORT", "5496"),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_LOCATION = "static"
STATIC_ROOT = BASE_DIR + "/static"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets')]

# CORS

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000"
]

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost"
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000"
]
