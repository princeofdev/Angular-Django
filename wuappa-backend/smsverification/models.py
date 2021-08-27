from datetime import timedelta

from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from model_utils.models import TimeStampedModel

from smsverification.validators import validate_phone_number


def generate_verification_code():
    return get_random_string(length=6).upper()


def generate_expiration_date():
    return timezone.now() + timedelta(minutes=15)


class VerificationCode(TimeStampedModel):

    phone = models.CharField(max_length=20, validators=[validate_phone_number])
    code = models.CharField(max_length=8, default=generate_verification_code)
    verification_date = models.DateTimeField(blank=True, null=True, default=None)
    expiration_date = models.DateTimeField(default=generate_expiration_date)

    def is_expired(self):
        return self.expiration_date < timezone.now()

    def is_verified(self):
        return self.verification_date is not None

    def verify(self):
        self.verification_date = timezone.now()
        self.save()
