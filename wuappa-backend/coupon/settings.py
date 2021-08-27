from django.utils.translation import ugettext_lazy as _

MONEY = 'MON'
DISCOUNT_RATE = 'DIS'

COUPON_TYPES = (
    (MONEY, _('Fixed amount off')),
    (DISCOUNT_RATE, _('% off')),
)