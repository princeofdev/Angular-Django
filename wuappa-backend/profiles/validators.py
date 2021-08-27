from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from geo.models import City


def validate_city(value):
    try:
        City.objects.get(id=value)
    except City.DoesNotExist:
        raise ValidationError(_("This city is not valid."))
