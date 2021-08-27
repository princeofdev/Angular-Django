from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class DayOff(models.Model):
    class Meta:
        unique_together = ("professional", "date")

    professional = models.ForeignKey(User, related_name='professional_days_off', verbose_name=_("Professional"))
    date = models.DateField()

    def __str__(self):
        return "Professional: %s. Date: %s" % (self.professional.email, self.date)
