"""
Django settings for project.
"""

import sys
import os
from base64 import b64decode
from datetime import timedelta


APPLICATION_STAGE = os.environ.get("APPLICATION_STAGE", "development")
APPLICATION_NAME = os.environ.get("APPLICATION_NAME", "assessment-scheduler")
SITE_ID = 1

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = os.path.join(BASE_DIR, ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "e@*pa*by5+7#m(t7q$2c2qq!dm)uv6my4qff3hd!ictf8$$+qh"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = APPLICATION_STAGE == "development"
TESTING = False

# Filters strings in hosts, removes empty ones
ALLOWED_HOSTS = list(
    filter(
        lambda _: len(_) > 0,
        os.environ.get("ALLOWED_HOSTS", "*").split(",")
    )
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.postgres",
    "django.contrib.admin",
    "corsheaders"
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "service.wsgi.application"


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# CUSTOM
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8080")
BASE_DOMAIN = os.environ.get("BASE_DOMAIN", "127.0.0.1:8080")
FRONT_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8080")


if APPLICATION_STAGE == "development":
    from .development import *

if APPLICATION_STAGE in ("staging", "production"):
    from .cloud import *

if "pytest" in sys.argv[0]:
    from .testing import *
else:
    try:
        from .local import *
    except ImportError:
        pass
