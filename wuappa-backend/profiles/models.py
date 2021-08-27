from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext as _
from django_iban.fields import IBANField, SWIFTBICField

from geo.models import WorkZone
from profiles.settings import PROFILE_TYPE, FINAL
from profiles.validators import validate_city
from services.models import UserService, Service
from smsverification.validators import validate_phone_number


class Profile(models.Model):
    user = models.OneToOneField(User)
    type = models.CharField(max_length=20, choices=PROFILE_TYPE, default=FINAL)
    phone = models.CharField(max_length=20, validators=[validate_phone_number])
    picture = models.URLField(null=True, blank=True)
    swift_bank_account = SWIFTBICField(null=True, blank=True)
    iban_bank_account = IBANField(null=True, blank=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    documents = ArrayField(models.URLField(), null=True, blank=True, help_text=_("Separate urls using a comma"))
    work_days = ArrayField(models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)]), null=True,
                           blank=True, help_text=_("Separate using a comma"))
    work_hours = ArrayField(models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)]), null=True,
                            blank=True, help_text=_("Separate using a comma"))
    city = ArrayField(models.IntegerField(null=True, blank=True, validators=[validate_city]), null=True, blank=True,
                      help_text=_("Separate using a comma"))
    rating = models.FloatField(default=0)
    fee = models.FloatField(default=0)
    language = models.CharField(max_length=7, default="en",  blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.user.email, self.type)


class UserWorkZone(models.Model):
    user = models.ForeignKey(User, related_name='users', verbose_name=_("User"))
    work_zone = models.ForeignKey(WorkZone, related_name='work_zones', verbose_name=_("WorkZone"))

    def __str__(self):
        return "%s - %s" % (self.user.email, self.work_zone.name)
