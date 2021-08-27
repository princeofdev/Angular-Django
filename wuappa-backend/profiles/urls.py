from allauth.account.views import ConfirmEmailView
from django.conf.urls import url
from rest_auth.registration.views import RegisterView, VerifyEmailView

from profiles.api import ResendVerificationView

urlpatterns = [
    url(r'^$', RegisterView.as_view(), name='rest_register'),
    url(r'^verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),
    url(r'^resend-verify-email/$', ResendVerificationView.as_view(), name='resend_verification_email'),
    url(r'^success/$', ConfirmEmailView.as_view(), name='account_email_verification_sent'),

    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(),
        name='account_confirm_email'),
]
