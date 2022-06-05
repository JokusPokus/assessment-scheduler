"""
Django settings for project.
"""

import sys
import os
from base64 import b64decode
from datetime import timedelta


APPLICATION_STAGE = os.environ.get('APPLICATION_STAGE', 'development')
APPLICATION_NAME = os.environ.get('APPLICATION_NAME', 'assessment-scheduler')
SITE_ID = 1

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = os.path.join(BASE_DIR, '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'e@*pa*by5+7#m(t7q$2c2qq!dm)uv6my4qff3hd!ictf8$$+qh'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = APPLICATION_STAGE == 'development'
TESTING = False

# Filters strings in hosts, removes empty ones
ALLOWED_HOSTS = list(
    filter(
        lambda _: len(_) > 0,
        os.environ.get('ALLOWED_HOSTS', '*').split(',')
    )
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.postgres',
    'django.contrib.admin',
    'corsheaders',
    'schedule.apps.ScheduleConfig',
    'core.apps.CoreConfig',
    'user.apps.UserConfig',
    'staff.apps.StaffConfig',
    'exam.apps.ExamConfig',
    'input.apps.InputConfig',
    'frontend',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend')],
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

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'user.User'
USERNAME_FIELD = 'email'

DJOSER = {
    'SEND_ACTIVATION_EMAIL': False,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'LOGOUT_ON_PASSWORD_CHANGE': True,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.MultiPartRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

WSGI_APPLICATION = 'service.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# CUSTOM
BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:8080')
BASE_DOMAIN = os.environ.get('BASE_DOMAIN', '127.0.0.1:8080')
FRONT_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:8080')


if APPLICATION_STAGE == 'development':
    from .development import *

if APPLICATION_STAGE in ('staging', 'production'):
    from .cloud import *

if 'pytest' in sys.argv[0]:
    from .testing import *
else:
    try:
        from .local import *
    except ImportError:
        pass
