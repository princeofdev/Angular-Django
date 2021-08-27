from cities_light.abstract_models import AbstractCountry, AbstractRegion, AbstractCity
from cities_light.receivers import connect_default_signals
from django.contrib.postgres.fields import ArrayField
from django.db.models import Model, CharField, ForeignKey, TextField
from django.utils.translation import ugettext as _
from model_utils import Choices
from model_utils.fields import StatusField

ACTIVE_STATUS = ('ACTIVE', 'Active')
INACTIVE_STATUS = ('ACTIVE', 'Active')
STATUS_CHOICES = Choices(('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'))


class Country(AbstractCountry):
    STATUS = STATUS_CHOICES
    status = StatusField()


class Region(AbstractRegion):
    STATUS = STATUS_CHOICES
    status = StatusField()


class City(AbstractCity):
    STATUS = STATUS_CHOICES
    status = StatusField()


# http://django-cities-light.readthedocs.io/en/stable-3.x.x/full.html#steps-to-customise-cities-light-models
connect_default_signals(Country)
connect_default_signals(Region)
connect_default_signals(City)


class WorkZone(Model):
    STATUS = STATUS_CHOICES
    city = ForeignKey(City)
    name = CharField(max_length=150)
    zip_codes = ArrayField(TextField(), help_text=_("Separate zip codes using a blank space"))
    status = StatusField()

    def __str__(self):
        return "%s - %s" % (self.name, self.city.name)
