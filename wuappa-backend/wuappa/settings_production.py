import os
from wuappa.settings_staging import *

DEBUG = False

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': os.environ.get('POSTGRES_DB', ''),
       'USER': os.environ.get('POSTGRES_USER', '')
   }
}

PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": "AAAAwhcrpTo:APA91bGawLlKuJlFm4VDc_Qozul9BAbzSoDnp_OZrZDdrYVy0eGW5c3TWv_7x5VkIUlvegUX7GW5pjHEevp7LrjIO5MZqdCdclTOyg52u1WwsEw_WlANCF9MkcKlCE4i6QVC09K2Ubyo",
    "FCM_ERROR_TIMEOUT": 60,
    "APNS_CERTIFICATE": os.path.join(BASE_DIR, "certs/wuappa_aps_production.pem"),
    "APNS_TOPIC": "com.telkia.wuappa",
    "APNS_USE_SANDBOX": False,
    "UPDATE_ON_DUPLICATE_REG_ID": True
}

STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY")
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY")
STRIPE_LIVE_MODE = True if os.environ.get("STRIPE_LIVE_MODE", None) != None else False
