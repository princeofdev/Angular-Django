from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from djstripe.models import Card


def check_credit_card(value):
    """
    Validates if the credit card number exist
    """
    if not Card.objects.filter(stripe_id=value).exists():
        raise ValidationError(_("Credit card id is not included in app."))
