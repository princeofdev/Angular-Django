from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.views import PasswordResetView

from profiles.serializers import CustomResetPassword


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class CustomPasswordResetView(PasswordResetView):
    serializer_class = CustomResetPassword
