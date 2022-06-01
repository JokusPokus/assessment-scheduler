import os
import environ
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(BASE_DIR, ".env")

DEBUG = False

# If a local .env doesn't exist, create one by loading it from Secret Manager.
if not os.path.isfile(env_file):
    import google.auth
    from google.cloud import secretmanager_v1 as sm

    _, project = google.auth.default()

    if project:
        client = sm.SecretManagerServiceClient()
        settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
        name = f"projects/{project}/secrets/{settings_name}/versions/latest"
        payload = client.access_secret_version(name=name).payload.data\
            .decode("UTF-8")

        with open(env_file, "w") as f:
            f.write(payload)

env = environ.Env()
env.read_env(env_file)

root = environ.Path(__file__) - 3
SITE_ROOT = root()

SECRET_KEY = env("SECRET_KEY")

if "CURRENT_HOST" in os.environ:
    # handle raw host(s), or http(s):// host(s), or no host.
    HOSTS = []
    for h in env.list("CURRENT_HOST"):
        if "://" in h:
            h = h.split("://")[1]
        HOSTS.append(h)
else:
    # Assume localhost if no CURRENT_HOST
    HOSTS = ["localhost"]


ALLOWED_HOSTS = [
                    "127.0.0.1",
                    "codescheduler-ckbpvgq2sq-ey.a.run.app/"
                ] + HOSTS

# CORS_ALLOWED_ORIGINS = []
# CSRF_TRUSTED_ORIGINS = []

# Storage
# define the default file storage for static files
STATICFILES_STORAGE = 'core.storage.backends.GoogleCloudStaticStorage'
GS_STATIC_BUCKET_NAME = 'codescheduler-media'
STATIC_URL = 'https://storage.googleapis.com/{}/'.format(GS_STATIC_BUCKET_NAME)


# Enable Django security precautions
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

DATABASES = {"default": env.db()}
