import uuid 
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from gift_card.settings import MONEY

def generate_primary_code():
    return str(uuid.uuid4())

class GiftCard(models.Model):
    code = models.CharField(primary_key=True, max_length=100, default=generate_primary_code, editable=False)
    amount_off = models.FloatField(help_text="Enter the amount of money to be deducted")
    type = models.CharField(max_length=20, default='MON', editable=False)
    redemption = models.DateTimeField(null=True, blank=True)
    valid = models.BooleanField(default=True)
    buyer = models.ForeignKey(User, related_name='buyer', null=True)
    gifted_to = models.ForeignKey(User, related_name='gifted_to', editable=False, null=True)
    used_amount = models.FloatField(default=0, editable=False)
    remaining_amount = models.FloatField(default=0, editable=False);

    def __str__(self):
        return self.code


class UsedGiftCard(models.Model):
    class Meta:
        unique_together = ("coupon", "transaction_id")

    coupon = models.ForeignKey('GiftCard', related_name='used_gift_card')
    user = models.ForeignKey(User, related_name='used_by')
    transaction_id = models.CharField(max_length=50, default=0)
    is_partial = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.coupon.code, self.user.email)
