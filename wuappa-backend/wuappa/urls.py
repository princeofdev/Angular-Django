from adminplus.sites import AdminSitePlus
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import refresh_jwt_token
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

from profiles.views import FacebookLogin, CustomPasswordResetView
from wuappa.viewsets import FCMDeviceAuthorizedViewSet

admin.site = AdminSitePlus()
admin.sites.site = admin.site
admin.autodiscover()

router = DefaultRouter()
router.register(r'device/apns', APNSDeviceAuthorizedViewSet)
router.register(r'device/gcm', FCMDeviceAuthorizedViewSet)

token_refresh_patterns = [
    url(r'^$', refresh_jwt_token),
]

facebook_patterns = [
    url(r'^', FacebookLogin.as_view(), name='fb_login'),
]

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^docs/', include('rest_framework_docs.urls')),

    # USERS AUTH
    url(r'^accounts/', include('allauth.urls')),  # Used for account-confirmation-email

    url(r'^api/1.0/token-refresh/', include(token_refresh_patterns)),
    url(r'^api/1.0/registration/', include('profiles.urls')),
    url(r'^api/1.0/facebook/', include(facebook_patterns)),
    url(r'^api/1.0/password/reset/$', CustomPasswordResetView.as_view(), name='rest_password_reset'),
    url(r'^api/1.0/', include('rest_auth.urls')),


    # API
    url(r'^api/', include('geo.urls')),
    url(r'^api/', include('files.urls')),
    url(r'^api/', include('smsverification.urls')),
    url(r'^api/', include('services.urls')),
    url(r'^api/', include('validations.urls')),
    url(r'^api/', include('work_calendars.urls')),
    url(r'^api/', include('credit_cards.urls')),
    url(r'^api/', include('coupon.urls')),
    url(r'^api/', include('gift_card.urls')),


    # DJ-STRIPE
    url(r'^payments/', include('djstripe.urls', namespace="djstripe")),

    # PUSH NOTIFICATIONS
    url(r'^api/1.0/', include(router.urls))
]
