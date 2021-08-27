from rest_framework import routers

from validations.views import PhoneValidatorViewSet, EmailValidatorViewSet, BankAccountValidatorViewSet

router = routers.SimpleRouter()

router.register(r'1.0/check-phone', PhoneValidatorViewSet, base_name='check-phone')
router.register(r'1.0/check-email', EmailValidatorViewSet, base_name='check-email')
router.register(r'1.0/check-bank-account', BankAccountValidatorViewSet, base_name='check-bank-account')

urlpatterns = router.urls
