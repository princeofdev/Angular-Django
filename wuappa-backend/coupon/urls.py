
from django.conf.urls import url

from coupon.api import CouponListAPI

urlpatterns = [
    url(r'1.0/coupon/(?P<code>[0-9a-zA-Z]+)', CouponListAPI.as_view(), name="coupon_api")
]