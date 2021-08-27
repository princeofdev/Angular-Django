from allauth.account.adapter import get_adapter as get_account_adapter, DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import ObjectDoesNotExist

from profiles.settings import PROFESSIONAL
from profiles.utils import ProfileOperator


class SocialAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login. In case of auto-signup,
        the signup form is not available.
        """
        user = sociallogin.user
        user.set_unusable_password()
        if form:
            get_account_adapter().save_user(request, user, form)
        else:
            get_account_adapter().populate_username(request, user)
        sociallogin.save(request)
        try:
            picture = user.socialaccount_set.first().get_avatar_url()
        except ObjectDoesNotExist:
            picture = None
        ProfileOperator.create_profile(user, {'picture': picture})
        return user


class AccountAdapter(DefaultAccountAdapter):

    def confirm_email(self, request, email_address):
        super(AccountAdapter, self).confirm_email(request, email_address)
        if email_address.user.profile.type == PROFESSIONAL:
            email_address.user.is_active = False
            email_address.user.save()

    def get_email_confirmation_redirect_url(self, request):
        response = super(AccountAdapter, self).get_email_confirmation_redirect_url(request)
        if request.POST.get('type') == 'PRO':
            response += '?type=PRO'
        return response
