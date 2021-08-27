from django.conf.urls import url

from smsverification.views import RequestVerificationAPIView, CodeVerificationAPIView

urlpatterns = [
    url(r'^1.0/sms-verification/request/$', RequestVerificationAPIView.as_view(), name='sms_verification_code_request'),
    url(r'^1.0/sms-verification/verify/$', CodeVerificationAPIView.as_view(), name='sms_verification_code_verify'),
]