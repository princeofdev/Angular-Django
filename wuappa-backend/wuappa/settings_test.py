import os
from wuappa.settings import *

if os.environ.get("POSTGRES_USER") and os.environ.get("POSTGRES_PASSWORD"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get("POSTGRES_DB", ""),
            'USER': os.environ.get("POSTGRES_USER", ""),
            'PASSWORD': os.environ.get("POSTGRES_PASSWORD", ""),
            'HOST': os.environ.get("POSTGRES_HOST", "127.0.0.1")
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get("POSTGRES_DB", "dev"),
			'USER': os.environ.get("POSTGRES_USER", "dev"),
            'PASSWORD': os.environ.get("POSTGRES_PASSWORD", "ubuntu"),
            'HOST': os.environ.get("POSTGRES_HOST", "127.0.0.1")
        }
    }

ALLOWED_HOSTS = ['206.189.182.9','127.0.0.1']
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "pk_test_xIvqLjEDd3iBrGIbGWYjkqgA")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "sk_test_SDcKtVxpxMlmsbUuqXVK2AEW")
STRIPE_LIVE_MODE = False

EMAIL_HOST = os.environ.get("EMAIL_HOST","smtp.gmail.com")
EMAIL_PORT = os.environ.get("EMAIL_PORT","587")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER","deepaksoni1909@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD","hdprtmboyvgzxrbw")
EMAIL_USE_TLS = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Wuappa: '
SMS_VERIFICATION["DEBUG"] = True
