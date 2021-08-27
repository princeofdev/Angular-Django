import os
from wuappa.settings import *

if os.environ.get("POSTGRES_USER") and os.environ.get("POSTGRES_PASSWORD"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get("POSTGRES_DB", ""),
            'USER': os.environ.get("POSTGRES_USER", ""),
            'PASSWORD': os.environ.get("POSTGRES_PASSWORD", ""),
            'HOST': os.environ.get("POSTGRES_HOST", "127.0.0.1"),
            'PORT': os.environ.get("POSTGRES_PORT", 5432)
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get("POSTGRES_DB", ""),
            'HOST': os.environ.get("POSTGRES_HOST", "127.0.0.1"),
            'PORT': os.environ.get("POSTGRES_PORT", 5432)
        }
    }

ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS", "*")]

STATIC_URL = os.environ.get("STATIC_URL", "/static/")
STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get("STATIC_ROOT", "static"))

MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")
MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get("MEDIA_ROOT", "media"))

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True if os.environ.get("EMAIL_USE_TLS", "True") == "True" else False

SMS_VERIFICATION["DEBUG"] = False

STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY")
STRIPE_LIVE_MODE = False

PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": "AAAAwhcrpTo:APA91bGawLlKuJlFm4VDc_Qozul9BAbzSoDnp_OZrZDdrYVy0eGW5c3TWv_7x5VkIUlvegUX7GW5pjHEevp7LrjIO5MZqdCdclTOyg52u1WwsEw_WlANCF9MkcKlCE4i6QVC09K2Ubyo",
    "FCM_ERROR_TIMEOUT": 60,
    "APNS_CERTIFICATE": os.path.join(BASE_DIR, "certs/wuappa_aps_production.pem"),
    "APNS_TOPIC": "com.telkia.wuappa",
    "APNS_USE_SANDBOX": False,
    "UPDATE_ON_DUPLICATE_REG_ID": True
}

LOGIN_REDIRECT_URL = 'account_login'
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''

if os.environ.get("ADMIN_EMAIL"):
    ADMINS = [('Wuappa', os.environ.get("ADMIN_EMAIL"))]

if os.environ.get("MANAGER_EMAIL"):
    MANAGERS = [('Wuappa', os.environ.get("MANAGER_EMAIL"))]

