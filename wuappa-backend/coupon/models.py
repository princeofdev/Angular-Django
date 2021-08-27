from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from coupon.settings import COUPON_TYPES, MONEY


class Coupon(models.Model):
    code = models.CharField(primary_key=True, max_length=100)
    amount_off = models.FloatField(help_text="Enter the amount of money or percentage to be deducted")
    type = models.CharField(max_length=20, choices=COUPON_TYPES)
    redemption = models.DateTimeField(null=True, blank=True)
    valid = models.BooleanField(default=True)

    def calculate_discount(self, qty):
        qty = float(qty)
        return qty - self.amount_off if self.type == MONEY else qty - (qty * self.amount_off / 100)

    def __str__(self):
        return self.code


class UsedCoupon(models.Model):
    class Meta:
        unique_together = ("coupon", "user")

    coupon = models.ForeignKey('Coupon', related_name='used_by')
    user = models.ForeignKey(User, related_name='used_coupons')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.coupon.code, self.user.email)
